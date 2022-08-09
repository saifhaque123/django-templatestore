import csv
import json
import sys
import psycopg2
import requests

def get_payload(filename, host, database, user, password):
    try:
        payload_list = []
        read_database = psycopg2.connect(host=host, database=database, user=user, password=password) # UAT database credentials

        read_cursor = read_database.cursor()

        with open(filename, "r") as templates_file:
            templates = csv.DictReader(templates_file)
            for template in templates:
                version = float(template["version"])
                name = template["name"]
                read_cursor.execute(
                    "select id, name, type, attributes from templatestore_template where name = '" + name + "'"
                )
                template_details = read_cursor.fetchall()

                read_cursor.execute(
                    "select id, sample_context_data from templatestore_template_version where template_id = '" + str(
                        template_details[0][0]) + "' and version = '" + str(version) + "'"
                )
                template_version_details = read_cursor.fetchall()

                read_cursor.execute(
                    "select id, data from templatestore_sub_template where template_version_id= '" + str(
                        template_version_details[0][0]) + "'"
                )
                sub_template_details = read_cursor.fetchall()

                sub_templates_list = []

                for sub_template in sub_template_details:
                    read_cursor.execute("select sub_type from templatestore_template_config where id = " + str(sub_template[0]))
                    config_details = read_cursor.fetchall()
                    sub_template_data = {
                        "sub_type": config_details[0][0],
                        "data": sub_template[1]
                    }
                    sub_templates_list.append(sub_template_data)

                data = {
                    "name": name,
                    "type": template_details[0][2],
                    "attributes": template_details[0][3],
                    "sample_context_data": template_version_details[0][1],
                    "sub_templates": sub_templates_list
                }
                payload_list.append(data)
        read_cursor.close()
        return payload_list
    except Exception as e:
        print(e)


def post_template(url, payload_list):
    for payload in payload_list:
        a = requests.post(url, data=json.dumps(payload))


def main():
    filename = sys.argv[1] # csv file name
    host = "acko-services-dev-rds.acko.in"
    database = "ackodev_templates"
    user = "ackodev_templates_rw_v1"
    password = "9qMzTLnHLhS7bQXDo3Gj"
    url = "api/v1/template"
    payload_list = get_payload(filename, host, database, user, password)
    post_template(url, payload_list) # will hit post template view endpoint and save the data in prod database if those credentials given in settings.py
    exit(0)


if __name__ == "__main__":
    main()