import shlex
from pathlib import Path
from typing import List

import yaml

from . import exceptions, file_contents, helpers, steps
from .configs import Config


def init_file_structure(config: Config):
    base_dir = config.base_dir
    if base_dir != '.':
        if not Path(base_dir).exists():
            Path(base_dir).mkdir()
    if not Path(base_dir, 'src').exists():
        Path(base_dir, 'src').mkdir()
        Path(base_dir, 'src', '__init__.py').touch()
        Path(base_dir, 'src', 'services').mkdir()
        Path(base_dir, 'src', 'services', '__init__.py').touch()
        service_create(base_dir, 'hello_world')
        service_create(base_dir, 'docs')
    if not Path(base_dir, 'api.yaml').exists():
        with open(f"{base_dir}/api.yaml", "w") as file:
            file.write(file_contents.api(
                title=config.api_title,
                description=config.api_description,
                project=config.gcp_project,
                region=config.gcp_region,
            ))
    if not Path(base_dir, 'requirements.txt').exists():
        with open(f"{base_dir}/requirements.txt", "w") as file:
            file.write(file_contents.requirements())


class Runtime:
    def __init__(self, config: Config, operation_id: str, **kwargs):
        self.config = config
        self.operation_id = operation_id
        self.entry_point = kwargs.get('entry_point', 'main')
        self.runtime = kwargs.get('runtime', 'python310')
        self.memory = kwargs.get('memory', '128MB')

    @property
    def command(self) -> str:
        return f'gcloud functions deploy --project="{self.config.gcp_project}" {self.operation_id} --trigger-http --runtime {self.runtime} --entry-point="{self.entry_point}" --memory={self.memory} --region="{self.config.gcp_region}"'


class Service:
    def __init__(self, operation_id: str, **kwargs):
        self.operation_id = operation_id
        self.summary = kwargs.get('summary', '')
        self.config = kwargs.get('config', None)
        self.runtime_config = None

    def runtime(self, config: Config) -> Runtime:
        with open(f'{config.base_dir}/{self.operation_id}.yaml') as f:
            service_config = yaml.safe_load(f.read())

        return Runtime(config, self.operation_id, **service_config)


def services_load(config: Config) -> dict:
    with open(f"{config.base_dir}/api.yaml") as f:
        data = yaml.safe_load(f)
    return data


def services_list(config: Config) -> List[Service]:
    data = services_load(config)
    services = list(data.get('paths', {}).values())
    services = [
        [Service(y.get('operationId'), summary=y.get('summary'), config=y) for y in x.values()]
        for x in services
    ]
    return [item for sublist in services for item in sublist]


def service_create(base_dir: str, service_name: str):
    if not Path(base_dir, 'src', 'services', f'{service_name}.py').exists():
        with open(f"{base_dir}/src/services/{service_name}.py", "w") as file:
            file.write(file_contents.service_lib(service_name))
    if not Path(base_dir, f'{service_name}.py').exists():
        with open(f"{base_dir}/{service_name}.py", "w") as file:
            file.write(file_contents.service_main(service_name))
    if not Path(base_dir, f'{service_name}.yaml').exists():
        with open(f"{base_dir}/{service_name}.yaml", "w") as file:
            file.write(file_contents.service_config(service_name))


def main(args) -> int:
    if not hasattr(args, 'which'):
        print(
            helpers.bcolors.FAIL
            + 'Can not parse action use --help'
            + helpers.bcolors.ENDC
        )
        return 1

    if hasattr(args, 'debug') and args.debug:
        print(args)

    config = Config()

    if args.which == 'init':
        config.base_dir = args.base_dir or helpers.ask_for('Base directory', '.')
        config.api_title = args.api_title or helpers.ask_for('API title', 'My API')
        config.api_description = args.api_description or helpers.ask_for('API description', 'My API description')
        config.gcp_project = args.gcp_project or helpers.ask_for('GCP project')
        config.gcp_region = args.gcp_region or helpers.ask_for('GCP region', 'europe-west2')
        config.save()
        init_file_structure(config)
        print(helpers.bcolors.OKGREEN + 'Init API-Gateway Config success' + helpers.bcolors.ENDC)
        return 0
    elif args.which == 'gateway':
        try:
            config.load()
        except exceptions.ConfigInvalidVersion:
            print(
                helpers.bcolors.FAIL
                + 'Config file is not compatible with this version. Please run `init` again.'
                + helpers.bcolors.ENDC
            )
            return 1
        if args.action == 'init':
            manager = steps.Manager(config, [
                steps.StepCommand(
                    shlex.split(
                        f'gcloud services enable apigateway.googleapis.com --project="{config.gcp_project}"'
                    )
                ),
                steps.StepCommand(
                    shlex.split(
                        f'gcloud services enable servicemanagement.googleapis.com --project="{config.gcp_project}"'
                    )
                ),
                steps.StepCommand(
                    shlex.split(
                        f'gcloud services enable servicecontrol.googleapis.com --project="{config.gcp_project}"'
                    )
                ),
                steps.StepCommand(
                    shlex.split(
                        f'gcloud services enable cloudbuild.googleapis.com --project="{config.gcp_project}"'
                    )
                ),
                steps.StepCommand(
                    shlex.split(
                        f'gcloud services enable cloudfunctions.googleapis.com --project="{config.gcp_project}"'
                    )
                ),
            ], simulate=args.simulate)
            rc = manager.run()
            if rc != 0:
                return rc
            print(helpers.bcolors.OKGREEN + 'Init API-Gateway success' + helpers.bcolors.ENDC)
            return 0
        elif args.action == 'deploy':
            config.deploy_version = config.deploy_version + 1
            api_id = config.api_title.lower().replace(' ', '-').replace('_', '-')
            api_config_id = f"v{config.deploy_version}"

            if config.deploy_version == 1:
                if args.debug:
                    print(f'Creating API Gateway {api_id}')
                commands = [
                    steps.StepCommand(
                        shlex.split(
                            f'gcloud api-gateway api-configs create {api_config_id} --api={api_id} --openapi-spec=api.yaml --project="{config.gcp_project}" --backend-auth-service-account="{config.gcp_project}@appspot.gserviceaccount.com"'
                        ),
                        work_dir=f'{config.base_dir}',
                    ),
                    steps.StepCommand(
                        shlex.split(
                            f'gcloud api-gateway gateways create {api_id} --api={api_id} --api-config={api_config_id} --location={config.gcp_region} --project="{config.gcp_project}"'
                        ),
                        work_dir=f'{config.base_dir}',
                    )
                ]
            else:
                if args.debug:
                    print(f'Updating API Gateway {api_id}')
                commands = [
                    steps.StepCommand(
                        shlex.split(
                            f'gcloud api-gateway api-configs create {api_config_id} --api={api_id} --openapi-spec=api.yaml --project="{config.gcp_project}" --backend-auth-service-account="{config.gcp_project}@appspot.gserviceaccount.com"'
                        ),
                        work_dir=f'{config.base_dir}',
                    ),
                    steps.StepCommand(
                        shlex.split(
                            f'gcloud api-gateway gateways update {api_id} --api={api_id} --api-config={api_config_id} --location={config.gcp_region} --project="{config.gcp_project}"'
                        ),
                        work_dir=f'{config.base_dir}',
                    )
                ]

            manager = steps.Manager(config, commands, simulate=args.simulate)
            rc = manager.run()
            if rc != 0:
                return rc
            print(helpers.bcolors.OKGREEN + 'Deploy API-Gatewway success' + helpers.bcolors.ENDC)
            config.save()
            return 0
    elif args.which == 'services':
        try:
            config.load()
        except exceptions.ConfigInvalidVersion:
            print(
                helpers.bcolors.FAIL
                + 'Config file is not compatible with this version. Please run `init` again.'
                + helpers.bcolors.ENDC
            )
            return 1
        if args.action == 'list':
            services = services_list(config)
            for service in services:
                print(service.operation_id, '-', service.summary)
            return 0
        elif args.action == 'create':
            services = [x for x in services_list(config) if x.operation_id == args.service]
            if len(services) > 0:
                print(
                    helpers.bcolors.FAIL
                    + f'Service {args.service} already exists'
                    + helpers.bcolors.ENDC
                )
                return 1
            service_create(config.base_dir, args.service)
            print(helpers.bcolors.OKGREEN + 'Service created' + helpers.bcolors.ENDC)
        elif args.action == 'describe':
            services = [x for x in services_list(config) if x.operation_id == args.service]
            if len(services) == 0:
                print(
                    helpers.bcolors.FAIL
                    + f'Service {args.service} not found'
                    + helpers.bcolors.ENDC
                )
                return 1
            print('Operation ID:', services[0].operation_id)
            print('Summary:', services[0].summary)
            return 0
        elif args.action == 'deploy':
            services = [x for x in services_list(config) if x.operation_id == args.service]
            if len(services) == 0:
                print(
                    helpers.bcolors.FAIL
                    + f'Service {args.service} not found'
                    + helpers.bcolors.ENDC
                )
                return 1

            service = services[0]
            print('# Deploy')

            service.runtime(config).command

            manager = steps.Manager(config, [
                steps.StepDeleteDir(f'{config.base_dir}/build/services/{service.operation_id}'),
                steps.StepCreatDir(f'{config.base_dir}/build/services/{service.operation_id}'),
                steps.StepCopyFileContent(
                    f'{config.base_dir}/requirements.txt',
                    f'{config.base_dir}/build/services/{args.service}/requirements.txt'
                ),
                steps.StepCopyFileContent(
                    f'{config.base_dir}/{service.operation_id}.py',
                    f'{config.base_dir}/build/services/{service.operation_id}/main.py'
                ),
                steps.StepCopyFileContent(
                    f'{config.base_dir}/api.yaml',
                    f'{config.base_dir}/build/services/{service.operation_id}/api.yaml'
                ),
                steps.StepCopyDir(
                    f'{config.base_dir}/src',
                    f'{config.base_dir}/build/services/{service.operation_id}/src'
                ),
                steps.StepCommand(
                    shlex.split(service.runtime(config).command),
                    work_dir=f'{config.base_dir}/build/services/{service.operation_id}',
                ),
            ], simulate=args.simulate)
            rc = manager.run()
            if rc != 0:
                return rc
            print(helpers.bcolors.OKGREEN + f'Deployed service {service.operation_id} success' + helpers.bcolors.ENDC)
            return 0
