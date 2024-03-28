API_PATH = {
    #############################################################
    #                   PLATFORM API TOKENS                     #
    #############################################################
    "validate_platform_token": "/v1/auth/validate",
    "create_platform_token": "/v1/auth/api-tokens/{name}",
    "list_platform_tokens": "/v1/auth/api-tokens",
    "revoke_platform_token": "/v1/auth/api-tokens/{name}",
    #############################################################
    #                        DATABASES                          #
    #############################################################
    "list_databases": "/v1/organizations/{org_name}/databases",
    "create_database": "/v1/organizations/{org_name}/databases",
    "delete_database": "/v1/organizations/{org_name}/databases/{name}",
    "retrieve_database": "/v1/organizations/{org_name}/databases/{name}",
    "update_database": "/v1/organizations/{org_name}/databases/{name}/configuration",
    "get_usage": "/v1/organizations/{org_name}/databases/{name}/usage",
    "get_stats": "/v1/organizations/{org_name}/databases/{name}/stats",
    "list_instances": "/v1/organizations/{org_name}/databases/{name}/instances",
    "retrieve_instance": "/v1/organizations/{org_name}/databases/{name}/instances/{instance_name}",
    "generate_db_token": "/v1/organizations/{org_name}/databases/{name}/auth/tokens",
    "invalidate_tokens": "/v1/organizations/{org_name}/databases/{name}/auth/rotate",
}
