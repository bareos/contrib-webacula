#!/bin/bash
#
# shell script to grant privileges to the bareos database
#

set -o errexit -o nounset

db_user=${db_user:-`/usr/sbin/webacula-config get_db_user`}
db_password=${db_password:-`/usr/sbin/webacula-config get_db_password`}
CMD=${CMD:-`/usr/sbin/webacula-config get_sql_cmd`}

ARG1=${1:-""}

DBUSER=""
if [ "$ARG1" != "readonly" ]; then
DBUSER="ALTER USER ${db_user} PASSWORD '${db_password}';"
fi

if [ "$ARG1" = "readonly" ]; then
    PERMISSION="SELECT"
    PERMISSION_SEQ="SELECT"
else
    PERMISSION="ALL"
    PERMISSION_SEQ="SELECT, UPDATE"
fi

TABLE_PERMISSIONS="
GRANT ${PERMISSION} ON webacula_logbook TO ${db_user};
GRANT ${PERMISSION} ON webacula_logtype TO ${db_user};
GRANT ${PERMISSION} ON webacula_jobdesc TO ${db_user};
GRANT ${PERMISSION} ON webacula_version TO ${db_user};
GRANT ${PERMISSION} ON webacula_users TO ${db_user};
GRANT ${PERMISSION} ON webacula_roles TO ${db_user};
GRANT ${PERMISSION} ON webacula_resources TO ${db_user};
GRANT ${PERMISSION} ON webacula_dt_resources TO ${db_user};
GRANT ${PERMISSION} ON webacula_client_acl TO ${db_user};
GRANT ${PERMISSION} ON webacula_command_acl TO ${db_user};
GRANT ${PERMISSION} ON webacula_dt_commands TO ${db_user};
GRANT ${PERMISSION} ON webacula_fileset_acl TO ${db_user};
GRANT ${PERMISSION} ON webacula_job_acl TO ${db_user};
GRANT ${PERMISSION} ON webacula_pool_acl TO ${db_user};
GRANT ${PERMISSION} ON webacula_storage_acl TO ${db_user};
GRANT ${PERMISSION} ON webacula_tmp_tablelist TO ${db_user};
GRANT ${PERMISSION} ON webacula_where_acl TO ${db_user};
GRANT ${PERMISSION} ON webacula_php_session TO ${db_user};
"

SEQUENCE_PERMISSIONS="
-- For sequences ON those tables
GRANT ${PERMISSION_SEQ} ON webacula_client_acl_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_command_acl_id_seq  TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_dt_commands_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_dt_resources_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_fileset_acl_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_job_acl_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_jobdesc_desc_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_logbook_logid_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_logtype_typeid_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_pool_acl_id_seq  TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_resources_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_roles_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_storage_acl_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_tmp_tablelist_tmpid_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_users_id_seq TO ${db_user};
GRANT ${PERMISSION_SEQ} ON webacula_where_acl_id_seq TO ${db_user};
"

printf "CMD: $CMD\n"
eval $CMD <<END-OF-DATA
${DBUSER}
${TABLE_PERMISSIONS}
${SEQUENCE_PERMISSIONS}
END-OF-DATA

res=$?
if test $res = 0; then
   echo "Privileges (${PERMISSION}) for user ${db_user} granted."
else
   echo "Error creating privileges."
fi
exit $res
