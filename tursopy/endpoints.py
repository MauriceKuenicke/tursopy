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
    "delete_database": "/v1/organizations/{org_name}/databases/{name}"
}
