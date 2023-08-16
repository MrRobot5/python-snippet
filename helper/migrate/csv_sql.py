import csv

"""
csv 文件转为 Insert SQL
使用场景：无法使用 HeidiSQL 工具的时候，可以使用文本操作来生成 SQL
@since 2023-08-15 11:36:19
"""

insert_template = "INSERT INTO foo_site_member_rel (id, is_delete, site_id, member_erp, member_name, member_dept, member_duty, is_sell_lead, member_phone, member_telephone, member_email, member_role, role, position, usf_org_code, permission_code_id, create_time, update_time, create_user, update_user, ts, src_corp_id, src_corp_name, sales_line, sales_line_site_id, wash_tag, yc_site_id) VALUES ({})"


def csv_to_insert_sql(csv_file):
    insert_values = []

    with open(csv_file, 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Skip header row

        for row in csv_data:
            row_values = [f"'{value}'" if value else 'NULL' for value in row]
            insert_values.append(', '.join(row_values))

    insert_sql = insert_template.format('), ('.join(insert_values))
    return insert_sql


if __name__ == '__main__':
    # 用法示例
    csv_file = 'C:/Users/yangpan3/Downloads/明细表_20230803173308.csv'
    insert_sql = csv_to_insert_sql(csv_file)
    print(insert_sql)
