#!/bin/sh
#
# shell script TO grant privileges to the bareos database
#
db_user=bareos #${db_user:-bareos}
bindir=/usr/bin
db_name=bareos #${db_name:-bareos}
db_password=
if [ "$db_password" != "" ]; then
   pass="password '$db_password'"
fi


$bindir/psql -f - -d ${db_name} $* <<END-OF-DATA


-- For tables
GRANT ALL ON webacula_logbook TO ${db_user};
GRANT ALL ON webacula_logtype TO ${db_user};
GRANT ALL ON webacula_jobdesc TO ${db_user};
GRANT ALL ON webacula_version TO ${db_user};
GRANT ALL ON webacula_users TO ${db_user};
GRANT ALL ON webacula_roles TO ${db_user};
GRANT ALL ON webacula_resources TO ${db_user};
GRANT ALL ON webacula_dt_resources TO ${db_user};
GRANT ALL ON webacula_client_acl TO ${db_user};
GRANT ALL ON webacula_command_acl TO ${db_user};
GRANT ALL ON webacula_dt_commands TO ${db_user};
GRANT ALL ON webacula_fileset_acl TO ${db_user};
GRANT ALL ON webacula_job_acl TO ${db_user};
GRANT ALL ON webacula_pool_acl TO ${db_user};
GRANT ALL ON webacula_storage_acl TO ${db_user};
GRANT ALL ON webacula_where_acl TO ${db_user};
GRANT ALL ON webacula_php_session TO ${db_user};

-- For sequences ON those tables
GRANT SELECT, UPDATE ON webacula_client_acl_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_command_acl_id_seq  TO ${db_user};
GRANT SELECT, UPDATE ON webacula_dt_commands_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_dt_resources_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_fileset_acl_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_job_acl_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_jobdesc_desc_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_logbook_logid_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_logtype_typeid_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_pool_acl_id_seq  TO ${db_user};
GRANT SELECT, UPDATE ON webacula_resources_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_roles_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_storage_acl_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_users_id_seq TO ${db_user};
GRANT SELECT, UPDATE ON webacula_where_acl_id_seq TO ${db_user};
END-OF-DATA
if [ $? -eq 0 ]
then
   echo "Privileges for user ${db_user} granted ON database ${db_name}."
   exit 0
else
   echo "Error creating privileges."
   exit 1
fi
