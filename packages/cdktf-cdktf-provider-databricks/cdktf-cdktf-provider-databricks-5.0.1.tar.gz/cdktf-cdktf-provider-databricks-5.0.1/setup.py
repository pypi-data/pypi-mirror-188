import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-databricks",
    "version": "5.0.1",
    "description": "Prebuilt databricks Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-databricks.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-databricks.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_databricks",
        "cdktf_cdktf_provider_databricks._jsii",
        "cdktf_cdktf_provider_databricks.aws_s3_mount",
        "cdktf_cdktf_provider_databricks.azure_adls_gen1_mount",
        "cdktf_cdktf_provider_databricks.azure_adls_gen2_mount",
        "cdktf_cdktf_provider_databricks.azure_blob_mount",
        "cdktf_cdktf_provider_databricks.catalog",
        "cdktf_cdktf_provider_databricks.cluster",
        "cdktf_cdktf_provider_databricks.cluster_policy",
        "cdktf_cdktf_provider_databricks.data_databricks_aws_assume_role_policy",
        "cdktf_cdktf_provider_databricks.data_databricks_aws_bucket_policy",
        "cdktf_cdktf_provider_databricks.data_databricks_aws_crossaccount_policy",
        "cdktf_cdktf_provider_databricks.data_databricks_catalogs",
        "cdktf_cdktf_provider_databricks.data_databricks_cluster",
        "cdktf_cdktf_provider_databricks.data_databricks_cluster_policy",
        "cdktf_cdktf_provider_databricks.data_databricks_clusters",
        "cdktf_cdktf_provider_databricks.data_databricks_current_user",
        "cdktf_cdktf_provider_databricks.data_databricks_dbfs_file",
        "cdktf_cdktf_provider_databricks.data_databricks_dbfs_file_paths",
        "cdktf_cdktf_provider_databricks.data_databricks_directory",
        "cdktf_cdktf_provider_databricks.data_databricks_group",
        "cdktf_cdktf_provider_databricks.data_databricks_instance_pool",
        "cdktf_cdktf_provider_databricks.data_databricks_job",
        "cdktf_cdktf_provider_databricks.data_databricks_jobs",
        "cdktf_cdktf_provider_databricks.data_databricks_mws_credentials",
        "cdktf_cdktf_provider_databricks.data_databricks_mws_workspaces",
        "cdktf_cdktf_provider_databricks.data_databricks_node_type",
        "cdktf_cdktf_provider_databricks.data_databricks_notebook",
        "cdktf_cdktf_provider_databricks.data_databricks_notebook_paths",
        "cdktf_cdktf_provider_databricks.data_databricks_schemas",
        "cdktf_cdktf_provider_databricks.data_databricks_service_principal",
        "cdktf_cdktf_provider_databricks.data_databricks_service_principals",
        "cdktf_cdktf_provider_databricks.data_databricks_share",
        "cdktf_cdktf_provider_databricks.data_databricks_shares",
        "cdktf_cdktf_provider_databricks.data_databricks_spark_version",
        "cdktf_cdktf_provider_databricks.data_databricks_sql_warehouse",
        "cdktf_cdktf_provider_databricks.data_databricks_sql_warehouses",
        "cdktf_cdktf_provider_databricks.data_databricks_tables",
        "cdktf_cdktf_provider_databricks.data_databricks_user",
        "cdktf_cdktf_provider_databricks.data_databricks_views",
        "cdktf_cdktf_provider_databricks.data_databricks_zones",
        "cdktf_cdktf_provider_databricks.dbfs_file",
        "cdktf_cdktf_provider_databricks.directory",
        "cdktf_cdktf_provider_databricks.entitlements",
        "cdktf_cdktf_provider_databricks.external_location",
        "cdktf_cdktf_provider_databricks.git_credential",
        "cdktf_cdktf_provider_databricks.global_init_script",
        "cdktf_cdktf_provider_databricks.grants",
        "cdktf_cdktf_provider_databricks.group",
        "cdktf_cdktf_provider_databricks.group_instance_profile",
        "cdktf_cdktf_provider_databricks.group_member",
        "cdktf_cdktf_provider_databricks.group_role",
        "cdktf_cdktf_provider_databricks.instance_pool",
        "cdktf_cdktf_provider_databricks.instance_profile",
        "cdktf_cdktf_provider_databricks.ip_access_list",
        "cdktf_cdktf_provider_databricks.job",
        "cdktf_cdktf_provider_databricks.library",
        "cdktf_cdktf_provider_databricks.metastore",
        "cdktf_cdktf_provider_databricks.metastore_assignment",
        "cdktf_cdktf_provider_databricks.metastore_data_access",
        "cdktf_cdktf_provider_databricks.mlflow_experiment",
        "cdktf_cdktf_provider_databricks.mlflow_model",
        "cdktf_cdktf_provider_databricks.mlflow_webhook",
        "cdktf_cdktf_provider_databricks.mount",
        "cdktf_cdktf_provider_databricks.mws_credentials",
        "cdktf_cdktf_provider_databricks.mws_customer_managed_keys",
        "cdktf_cdktf_provider_databricks.mws_log_delivery",
        "cdktf_cdktf_provider_databricks.mws_networks",
        "cdktf_cdktf_provider_databricks.mws_permission_assignment",
        "cdktf_cdktf_provider_databricks.mws_private_access_settings",
        "cdktf_cdktf_provider_databricks.mws_storage_configurations",
        "cdktf_cdktf_provider_databricks.mws_vpc_endpoint",
        "cdktf_cdktf_provider_databricks.mws_workspaces",
        "cdktf_cdktf_provider_databricks.notebook",
        "cdktf_cdktf_provider_databricks.obo_token",
        "cdktf_cdktf_provider_databricks.permission_assignment",
        "cdktf_cdktf_provider_databricks.permissions",
        "cdktf_cdktf_provider_databricks.pipeline",
        "cdktf_cdktf_provider_databricks.provider",
        "cdktf_cdktf_provider_databricks.provider_resource",
        "cdktf_cdktf_provider_databricks.recipient",
        "cdktf_cdktf_provider_databricks.repo",
        "cdktf_cdktf_provider_databricks.schema",
        "cdktf_cdktf_provider_databricks.secret",
        "cdktf_cdktf_provider_databricks.secret_acl",
        "cdktf_cdktf_provider_databricks.secret_scope",
        "cdktf_cdktf_provider_databricks.service_principal",
        "cdktf_cdktf_provider_databricks.service_principal_role",
        "cdktf_cdktf_provider_databricks.service_principal_secret",
        "cdktf_cdktf_provider_databricks.share",
        "cdktf_cdktf_provider_databricks.sql_dashboard",
        "cdktf_cdktf_provider_databricks.sql_endpoint",
        "cdktf_cdktf_provider_databricks.sql_global_config",
        "cdktf_cdktf_provider_databricks.sql_permissions",
        "cdktf_cdktf_provider_databricks.sql_query",
        "cdktf_cdktf_provider_databricks.sql_visualization",
        "cdktf_cdktf_provider_databricks.sql_widget",
        "cdktf_cdktf_provider_databricks.storage_credential",
        "cdktf_cdktf_provider_databricks.table",
        "cdktf_cdktf_provider_databricks.token",
        "cdktf_cdktf_provider_databricks.user",
        "cdktf_cdktf_provider_databricks.user_instance_profile",
        "cdktf_cdktf_provider_databricks.user_role",
        "cdktf_cdktf_provider_databricks.workspace_conf"
    ],
    "package_data": {
        "cdktf_cdktf_provider_databricks._jsii": [
            "provider-databricks@5.0.1.jsii.tgz"
        ],
        "cdktf_cdktf_provider_databricks": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdktf>=0.15.0, <0.16.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.73.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
