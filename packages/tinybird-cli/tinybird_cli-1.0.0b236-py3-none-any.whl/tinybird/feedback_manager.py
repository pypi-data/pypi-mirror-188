from collections import namedtuple

FeedbackMessage = namedtuple('FeedbackMessage', 'message')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    CGREY = '\33[90m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_message(message, color=bcolors.ENDC):
    def formatter(**kwargs):
        return f"{color}{message.format(**kwargs)}{bcolors.ENDC}"

    return formatter


def error_message(message):
    return print_message(f"\n** {message}", bcolors.FAIL)


def simple_error_message(message):
    return print_message(f"{message}", bcolors.FAIL)


def warning_message(message):
    return print_message(message, bcolors.WARNING)


def info_message(message):
    return print_message(message)


def info_highlight_message(message):
    return print_message(message, bcolors.OKBLUE)


def success_message(message):
    return print_message(message, bcolors.OKGREEN)


def prompt_message(message):
    return print_message(message, bcolors.HEADER)


class FeedbackManager:
    error_exception = error_message("{error}")
    error_exception_trace = error_message("{error}\n** Trace:\n{trace}")
    error_notoken = error_message("No auth token provided. Run 'tb auth' to configure them or re-run the command passing the --token param (example: tb --token <the_token> datasource ls).")
    error_auth_config = error_message("{config_file} does not exist")
    error_file_config = error_message("{config_file} can't be written, check write permissions on this folder")
    error_load_file_config = error_message("{config_file} can't be loaded, remove it and run the command again")
    error_push_file_exception = error_message('Failed running {filename}: {error}')
    error_parsing_node = error_message("error parsing node \"{node}\" from pipe \"{pipe}\": {error}")
    error_check_pipe = error_message("check error: {error}")
    error_pipe_already_exists = error_message("{pipe} already exists")
    error_datasource_already_exists = error_message("{datasource} already exists")
    error_datasource_already_exists_and_alter_failed = error_message("{datasource} already exists and the migration can't be executed to match the new definition: {alter_error_message}")
    error_datasource_can_not_be_deleted = error_message("{datasource} cannot be deleted:\n** {error}")
    error_job_status = error_message("Job status at {url} cannot be retrieved")
    error_removing_datasource = error_message("Failed removing Data Source {datasource}")
    error_creating_datasource = error_message("Failed creating Data Source: {error}")
    error_processing_data = error_message("{error} - FAIL")
    error_file_already_exists = error_message("{file} already exists, use --force to override")
    error_invalid_token_for_host = error_message("Invalid token for {host}")
    error_invalid_token = error_message("Invalid token")
    error_invalid_query = error_message("Only SELECT queries are supported")
    error_pipe_does_not_exist = error_message("'{pipe}' pipe does not exist")
    error_datasource_does_not_exist = error_message("'{datasource}' Data Source does not exist")
    error_pull = error_message("there was a problem while pulling: {error}")
    error_parsing_file = error_message("error parsing {filename}:{lineno} {error}")
    error_parsing_schema = error_message("error parsing schema (line {line}): {error}")
    error_sorting_key = error_message("SORTING_KEY should be set with {engine}")
    error_unknown_resource = error_message("Unknown resource '{resource}'")
    error_file_extension = error_message("File extension for {filename} not supported. It should be one of .datasource or .pipe")
    error_remove_endpoint = error_message("Failed removing pipe endpoint {error}")
    error_remove_no_endpoint = error_message("Pipe does not have any endpoint")
    error_updating_pipe = error_message("Failed updating pipe {error}")
    error_removing_node = error_message("Failed removing node from pipe {pipe}: {error}")
    error_pushing_pipe = error_message("Failed pushing pipe {pipe}: {error}")
    error_creating_endpoint = error_message("Failed creating endpoint in node {node} on pipe {pipe}: {error}")
    error_creating_pipe = error_message("Failed creating pipe {error}")
    error_removing_dummy_node = error_message("Failed removing node {error}")
    error_check_pipes_populate = error_message("You can't check pipes with populate=True")
    error_check_pipes_api = error_message("Error retrieving most common {pipe} requests to run automatic regression tests, you can bypass checks by running push with the --no-check flag")
    error_negative_version = error_message("VERSION gets one positive integer param")
    error_while_running_job = error_message("Error while running job: {error}")
    error_getting_job_info = error_message("Error while getting job status:\n{error}\n\nThe job should still be running. Check => {url}")
    error_while_check_materialized = error_message("Invalid results, read description below to fix the error: {error}")
    error_auth = error_message("Check your local config")
    error_wrong_config_file = error_message("Wrong {config_file}, run 'tb auth' to initialize")
    error_workspace_not_in_local_config = error_message("Use 'tb auth add --ws {workspace}' to add this workspace to the local config")
    error_not_personal_auth = error_message("** You have to authenticate with a personal account")
    error_incremental_not_supported = error_message("The --incremental parameter is only supported when the `--connector` parameter is passed")
    error_invalid_connector = error_message("Invalid connector parameter: Use one of {connectors}")
    error_connector_not_configured = error_message("{connector} connector not properly configured. Please run `tb auth --connector {connector}` first")
    error_connector_not_installed = error_message("{connector} connector not properly installed. Please run `pip install tinybird-cli[{connector}]` first")
    error_option = error_message("{option} is not a valid option")
    error_job_does_not_exist = error_message("Job with id '{job_id}' does not exist")
    error_job_cancelled_but_status_unknown = error_message("Job with id '{job_id}' has started the cancellation process but its status is unknown.")
    error_kafka_bootstrap_server = error_message("Invalid bootstrap_server")
    error_kafka_bootstrap_server_conn = error_message("Cannot connect to bootstrap_server.\nPlease, check host, port, and connectivity, including any firewalls.")
    error_kafka_bootstrap_server_conn_timeout = error_message("Cannot connect to bootstrap_server, connection timed out.\nPlease, check host, port, and connectivity, including any firewalls.")
    error_kafka_registry = error_message("Invalid kafka registry URL")
    error_kafka_topic = error_message("Invalid kafka topic")
    error_kafka_group = error_message("Invalid kafka group ID")
    error_kafka_auto_offset_reset = error_message('Invalid kafka auto.offset.reset config. Valid values are: ["earliest", "latest", "error"]')
    error_datasource_name = error_message("Invalid Data Source name")
    error_datasource_connection_id = error_message("Invalid connection ID")
    error_connection_does_not_exists = error_message("Connection {connection_id} does not exist")
    error_connection_create = error_message("Connection {connection_name} could not be created: {error}")
    error_workspace = error_message("Workspace {workspace} not found. use 'tb workspace ls' to list your workspaces")
    error_branch = error_message("Branch {branch} not found. use 'tb branch ls' to list your branches, make sure you are authenticated using the right workspace token")
    error_not_a_branch = error_message("To use this command you need to be authenticated on a branch. Use 'tb branch ls' and 'tb branch use' and retry the command.")
    error_not_allowed_in_branch = error_message("Command disabled for branches")
    error_getting_region_by_index = error_message("Unable to get region by index, list available regions using 'tb auth ls'")
    error_region_index = error_message("Error selecting region '{host_index}', available options are: {available_options} or 0")
    error_getting_region_by_name_or_url = error_message("Unable to get region by name or host url, list available regions using 'tb auth ls'")
    error_operation_can_not_be_performed = error_message("Operation can not be performed: {error}")
    error_partial_replace_cant_be_executed = error_message("A partial replace can't be executed in the '{datasource}' Data Source.")
    error_push_fixture_will_replace_data = error_message("Data Source '{datasource}' already has data. To override it, use --force")
    error_datasource_ls_type = error_message("Invalid Format provided")
    error_pipe_ls_type = error_message("Invalid Format provided")
    error_token_not_validate_in_any_region = error_message("Token not validated in any region")
    error_not_authenticated = error_message("You are not authenticated, use 'tb auth -i' to authenticate yourself")
    error_checking_templates = error_message("Unable to retrieve list of available starter kits")
    error_starterkit_index = error_message("Error selecting starter kit '{starterkit_index}'. Select a valid index or 0 to cancel")
    error_starterkit_name = error_message("Unknown starter kit '{starterkit_name}'")
    error_missing_url_or_connector = error_message("Missing url, local path or --connector argument for append to datasource '{datasource}'")
    error_no_test_results = error_message("Error: No test results to show")
    error_running_test = error_message("There was a problem running test file {file} (use -v for more info)")
    error_processing_blocks = error_message("There was been an error while processing some blocks: {error}")
    error_switching_to_main = error_message("** Unable to switch to main. Need to authenticate again, use 'tb auth")

    prompt_choose = prompt_message("=> Choose one of the above options to continue... ")
    prompt_choose_node = prompt_message("=> Please, select a node to materialize... ")
    prompt_populate = prompt_message("Do you want to populate the materialized view with existing data? (It'll truncate the materialized view before population starts)")

    prompt_ws_name = prompt_message('❓ Workspace name:')
    prompt_ws_template = prompt_message('❓ Starter template:')

    warning_beta_tester = warning_message("This feature is under development and released as a beta version. You can report any feedback (bugs, feature requests, etc.) to support@tinybird.co")
    warning_connector_not_installed = warning_message("Auth found for {connector} connector but it's not properly installed. Please run `pip install tinybird-cli[{connector}]` to use it")
    warning_deprecated = warning_message("** [DEPRECATED]: {warning}")
    warning_token_pipe = warning_message("** There's no read token for pipe {pipe}")
    warning_file_not_found_inside = warning_message("** Warning: {name} not found inside: \n   - {folder}\n   - {folder}/datasources\n   - {folder}/endpoints")
    warning_check_pipe = warning_message("** Warning: Failed removing checker pipe: {content}")
    single_warning_materialized_pipe = warning_message("⚠️  {content} For more information read {docs_url} or contact us at support@tinybird.co")
    warning_datasource_already_exists = warning_message(
        """** Warning: Data Source {datasource} already exists and can't be migrated or replaced.
** This is a safety feature to avoid removing a Data Source by mistake.
** Drop it using:
**    $ tb datasource rm {datasource}""")
    warning_name_already_exists = warning_message("** Warning: {name} already exists, skipping")
    warning_dry_name_already_exists = warning_message("** [DRY RUN] {name} already exists, skipping")
    warning_file_not_found = warning_message("** Warning: {name} file not found")
    warning_update_version = warning_message("** UPDATE AVAILABLE: please run \"pip install tinybird-cli=={latest_version}\" to update")
    warning_current_version = warning_message("** current: tinybird-cli {current_version}\n")
    warning_confirm_truncate_datasource = prompt_message("Do you want to truncate {datasource}? Once truncated, your data can't be recovered")
    warning_confirm_delete_datasource = prompt_message("{dependencies_information} {warning_message}")
    warning_confirm_delete_rows_datasource = prompt_message("Do you want to delete {datasource}'s rows matching condition \"{delete_condition}\"? Once deleted, they can't be recovered")
    warning_confirm_delete_pipe = prompt_message("Do you want to remove the pipe \"{pipe}\"?")
    warning_confirm_drop_prefix = prompt_message("Do you want to remove all pipes and Data Sources with prefix \"{prefix}\"?")
    warning_confirm_clear_workspace = prompt_message("Do you want to remove all pipes and Data Sources from this workspace?")
    warning_confirm_delete_workspace = prompt_message("Do you want to remove this workspace?")
    warning_confirm_delete_branch = prompt_message("Do you want to remove '{branch}' branch?")
    warning_datasource_is_connected = warning_message("** Warning: '{datasource}' Data Source is connected to {connector}. If you delete it, it will stop consuming data")
    warning_workspaces_admin_token = warning_message("** Warning: you're using an admin token that is not associated with any user. If you want to be able to switch between workspaces, please use an admin token associated with your account.")
    warning_development_cli = warning_message("** Using CLI in development mode\n")
    warning_token_scope = warning_message("** Warning: This token is not an admin token")
    warning_parquet_fixtures_not_supported = warning_message("** Warning: generating fixtures for Parquet files is not supported")
    warning_datasource_share = warning_message("** Warning: Do you want to share the datasource {datasource} from the workspace {source_workspace} to {destination_workspace}")
    warning_users_dont_exist = warning_message("** Warning: The following users do not exist in the workspace {workspace}: {users}")
    warning_user_doesnt_exist = warning_message("** Warning: The user {user} does not exist in the workspace {workspace}")
    warning_skipping_include_file = warning_message("** Warning: Skipping {file} as is an included file")
    warning_disabled_ssl_checks = warning_message("** Warning: Running with TB_DISABLE_SSL_CHECKS")

    info_materialize_push_datasource_exists = warning_message('** Data Source {name} already exists')
    info_materialize_push_datasource_override = prompt_message('Delete the Data Source from the workspace and push {name} again?')
    info_materialize_push_pipe_skip = info_message('  [1] Push {name} and override if it exists')
    info_materialize_push_pipe_override = info_message('  [2] Push {name} and override if it exists with no checks')
    info_materialize_populate_partial = info_message('  [1] Partially populate: Uses a 10 percent subset of the data or a maximum of 2M rows to quickly validate the materialized view')
    info_materialize_populate_full = info_message('  [2] Fully populate')
    info_pipe_backup_created = info_message("** Created backup file with name {name}")
    info_before_push_materialize = info_message("** Pushing the pipe {name} to your workspace to analyze it")
    info_before_materialize = info_message("** Analyzing the pipe {name}")
    info_pipe_exists = prompt_message("** A pipe with the name {name} already exists, do you want to override it?")
    prompt_override = prompt_message("** Do you want to try override it?")
    prompt_override_local_file = prompt_message("** Do you want to override {name} with the formatted version shown above?")
    info_populate_job_url = info_message("** Populating job url {url}")
    info_data_branch_job_url = info_message("** Data Branch job url {url}")
    info_populate_subset_job_url = info_message("** Populating (subset {subset}) job url {url}")
    info_populate_condition_job_url = info_message("** Populating with --sql-condition `{populate_condition}` => job url {url}")
    info_create_not_found_token = info_message("** Token {token} not found, creating one")
    info_create_found_token = info_message("** Token {token} found, adding permissions")
    info_populate_job = info_message("** Populating job ({job}) {progress}- {status}")
    info_building_dependencies = info_message("** Building dependencies")
    info_processing_new_resource = info_message("** Running {name} {version}")
    info_dry_processing_new_resource = info_message("** [DRY RUN] Running {name} {version}")
    info_processing_resource = info_message("** Running {name} => v{version} (remote latest version: v{latest_version})")
    info_dry_processing_resource = info_message("** [DRY RUN] Running {name} => v{version} (remote latest version: v{latest_version})")
    info_pushing_fixtures = info_message("** Pushing fixtures")
    info_not_pushing_fixtures = info_message("** Not pushing fixtures")
    info_checking_file = info_message("** Checking {file}")
    info_checking_file_size = info_message("** Checking {filename} (appending {size})")
    info_no_rows = info_message("** No rows")
    info_processing_file = info_message("** Processing {filename}")
    info_skip_already_exists = print_message("    => skipping, already exists")
    info_dependency_list = info_message("** {dependency}")
    info_dependency_list_item = info_message("** --- {dependency}")
    info_no_dependencies_found = info_message("** No dependencies found for {dependency}")
    info_no_compatible_dependencies_found = info_message("** Data Sources with incompatible partitions found:")
    info_admin_token = info_message("** Go to {host}/tokens, copy the admin token and paste it")
    info_append_data = info_message("** => If you want to insert data use: $ tb datasource append")
    info_datasources = info_message("** Data Sources:")
    info_connections = info_message("** Connections:")
    info_query_stats = print_message("** Query took {seconds} seconds\n** Rows read: {rows}\n** Bytes read: {bytes}")
    info_datasource_title = print_message("** {title}", bcolors.BOLD)
    info_datasource_row = info_message("{row}")
    info_datasource_delete_rows_job_url = info_message("** Delete rows job url {url}")
    info_pipes = info_message("** Pipes:")
    info_pipe_name = info_message("** - {pipe}")
    info_using_node = print_message("** Using last node {node} as endpoint")
    info_removing_datasource = info_message("** Removing Data Source {datasource}")
    info_removing_datasource_not_found = info_message("** {datasource} not found")
    info_dry_removing_datasource = info_message("** [DRY RUN] Removing Data Source {datasource}")
    info_removing_pipe = info_message("** Removing pipe {pipe}")
    info_removing_pipe_not_found = info_message("** {pipe} not found")
    info_dry_removing_pipe = info_message("** [DRY RUN] Removing pipe {pipe}")
    info_path_created = info_message("** - /{path} created")
    info_path_already_exists = info_message("** - /{path} already exists, skipping")
    info_writing_resource = info_message("** Writing {resource} {prefix}")
    info_skipping_resource = info_message("** Skipping {resource}")
    info_writing_datasource = info_message("[D] writing {datasource}")
    info_starting_import_process = info_message("** \N{egg} starting import process")
    info_progress_blocks = info_message("\N{egg} blocks")
    info_progress_current_blocks = info_message("\N{hatching chick} blocks")
    info_jobs = info_message("** Jobs:")
    info_workspaces = info_message("** Workspaces:")
    info_branches = info_message("** Branches:")
    info_current_workspace = info_message("** Current workspace:")
    info_current_branch = info_message("** Current branch:")
    info_job = info_message("  ** Job: {job}")
    info_data_pushed = info_message("** Data pushed to {datasource}")
    info_materialized_datasource_created = info_message("** Materialized pipe '{pipe}' created the Data Source '{datasource}'")
    info_materialized_datasource_used = info_message("** Materialized pipe '{pipe}' using the Data Source '{datasource}'")
    info_no_pipes_stats = info_message("** No pipe stats")
    info_starting_export_process = info_message("** \N{Chicken} starting export process from {connector}")
    info_ask_for_datasource_confirmation = info_message('** Please type the Data Source name to be replaced')
    info_datasource_doesnt_match = info_message("** The description or schema of '{datasource}' has changed.")
    info_ask_for_alter_confirmation = info_message('** Please confirm you want to apply the changes above y/N')
    info_available_regions = info_message('** List of available regions:')
    info_trying_authenticate = info_message('** Trying to authenticate with {host}')
    info_auth_cancelled_by_user = info_message('** Auth cancelled by user.')
    info_user_already_exists = info_message("** The user '{user}' already exists in {workspace_name}")
    info_users_already_exists = info_message('** All users already exist in {workspace_name}')
    info_user_not_exists = info_message("** The user '{user}' doesn't exist in {workspace_name}.")
    info_users_not_exists = info_message("** These users don't exist in {workspace_name}.")
    info_cancelled_by_user = info_message('** Cancelled by user.')

    info_workspace_create_greeting = info_message('Please enter the name for your new workspace. Remember the name you choose must be unique, you can add a suffix in case of collision.\nYou can bypass this step by supplying it after the command.')
    info_create_ws_msg_template = info_message('Now let\'s pick a starter template! 🐣\nStarter template are pre-built data projects for different use cases, that you can use as a starting point and then build on top of that.\nYou can bypass this step by supplying a value for the --starter-kit option.')
    info_workspace_branch_create_greeting = info_message('Please enter the name for your new workspace branch. Remember the name you choose must be unique, you can add a suffix in case of collision.\nYou can bypass this step by supplying a value for the --name option.')

    success_test_endpoint = success_message("** => Test endpoint with:\n** $ curl {host}/v0/pipes/{pipe}.json?token={token}")
    success_test_endpoint_no_token = success_message("** => Test endpoint at {host}/v0/pipes/{pipe}.json")
    success_processing_data = success_message("**  OK")
    success_generated_file = success_message(
        """** Generated {file}
** => Create it on the server running: $ tb push {file}
** => Append data using: $ tb datasource append {stem} {filename}
""")
    success_generated_pipe = success_message(
        """** Generated {file}
** => Create it on the server running: $ tb push {file}
""")
    success_generated_matview = success_message(
        """** Generated destination Data Source for materialized node {node_name} -> {file}
** => Check everything is correct before and create it on the server running: $ tb push {file}
""")
    success_generated_local_file = success_message("** => Saved local file {file}")
    success_generated_fixture = success_message("** => Generated fixture {fixture}")
    success_processing_file = success_message("** => File {filename} processed correctly")
    success_appended_rows = success_message("** Appended {appended_rows} new rows")
    success_total_rows = success_message("** Total rows in {datasource}: {total_rows}")
    success_appended_datasource = success_message("** Data appended to Data Source '{datasource}' successfully!")
    success_replaced_datasource = success_message("** Data replaced in Data Source '{datasource}' successfully!")
    success_auth = success_message("** Auth successful! \n** Configuration written to .tinyb file, consider adding it to .gitignore")
    success_auth_added = success_message("** Auth config added!")
    success_auth_removed = success_message("** Auth config removed")
    success_delete_datasource = success_message("** Data Source '{datasource}' deleted")
    success_truncate_datasource = success_message("** Data Source '{datasource}' truncated")
    success_delete_rows_datasource = success_message("** Data Source '{datasource}' rows deleted matching condition \"{delete_condition}\"")
    success_delete_pipe = success_message("** Pipe '{pipe}' deleted")
    success_created_matview = success_message(
        """** Materialized view {name} created!
** Materialized views work as insert triggers, anytime you append data into the source Data Source the materialized node query will be triggered.
""")
    success_created_pipe = success_message(
        """** New pipe created!
** Node id: {node_id})
** Set node as endpoint with:
**   $ tb pipe set_endpoint {pipe} {node_id}
** Pipe URL: {host}/v0/pipes/{pipe}
""")
    success_node_changed = success_message("** New node: {node_id}\n    => pipe: {pipe_name_or_uid}\n    => name: {node_name}")
    success_node_published = success_message(
        """** Endpoint published!
** Pipe URL: {host}/v0/pipes/{pipe}
""")
    success_node_unpublished = success_message(
        """** Endpoint unpublished!
** Pipe URL: {host}/v0/pipes/{pipe}
""")
    success_print_pipe = success_message("** Pipe: {pipe}")
    success_create = success_message("** '{name}' created")
    success_progress_blocks = success_message("** \N{front-facing baby chick} done")
    success_now_using_config = success_message("** Now using {name} ({id})")
    success_connector_config = success_message("** {connector} configuration written to {file_name} file, consider adding it to .gitignore")
    success_job_cancellation_cancelled = success_message("** Job with id '{job_id}' has been cancelled")
    success_job_cancellation_cancelling = success_message(
        "** Job with id '{job_id}' is now in cancelling status and will be cancelled eventually")
    success_datasource_alter = success_message("** The Data Source has been correctly updated.")
    success_datasource_kafka_connected = success_message("** Data Source '{id}' created\n"
                                                         "** Kafka streaming connection configured successfully!")
    success_datasource_shared = success_message("** The Data Source {datasource} has been correctly shared with {workspace}")
    success_connection_created = success_message("** Connection {id} created successfully!")
    success_delete_connection = success_message("** Connection {connection_id} removed successfully")
    success_connection_creating = success_message("** Creating new Kafka connection '{connection_name}'")
    success_connection_using = success_message("** Using connection '{connection_name}'")
    success_using_host = success_message('** Using host: {host} ({name})')
    success_workspace_created = success_message("** Workspace '{workspace_name}' has been created")
    success_workspace_branch_created = success_message("** Branch '{branch_name}' from '{workspace_name}' has been created")
    success_workspace_data_branch = success_message("** Partitions from origin Workspace have been attached to the branch Workspace")

    success_workspace_deploying_template = success_message("Deploying your new '{workspace_name}' workspace, using the '{template}' template:")
    success_workspace_deleted = success_message("** Workspace '{workspace_name}' deleted")
    success_branch_deleted = success_message("** Branch '{branch_name}' deleted")
    success_workspace_user_added = success_message("** User {user} added to workspace '{workspace_name}'")
    success_workspace_users_added = success_message("** Users added to workspace '{workspace_name}'")
    success_workspace_user_removed = success_message("** User {user} removed from workspace '{workspace_name}'")
    success_workspace_users_removed = success_message("** Users removed from workspace '{workspace_name}'")
    success_workspace_user_changed_role = success_message("** {user}'s role setted to {role} in '{workspace_name}'")
    success_workspace_users_changed_role = success_message("** Users' role setted to {role} in '{workspace_name}'")

    success_test_added = success_message("** Test added successfully")
    success_remember_api_host = success_message('** Remember to use {api_host} in all your API calls.')

    debug_running_file = print_message("** Running {file}", bcolors.CGREY)
