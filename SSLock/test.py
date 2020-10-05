from SSLock import General

OUTPUT_KEYS = General.output_run_cmd("curl -s https://api.wordpress.org/secret-key/1.1/salt/").decode("utf-8").split("');")
for key in OUTPUT_KEYS:
    if key.strip() == '': OUTPUT_KEYS.remove(key)
OUTPUT_KEYS_DICT = dict()
for index, key in enumerate(OUTPUT_KEYS):
    index += 1
    OUTPUT_KEYS_DICT["_" + str(index)] = [
        '( '.join(key.split(",")[0].split('(')).strip() + ',',
        key.strip() + "');\n"
    ]
General.change_lines(
    'test.txt',
    **OUTPUT_KEYS_DICT
)
General.change_lines(
    'test.txt',
    _1=["define( 'DB_NAME',", f"define( 'DB_NAME', 'DB_NAME');"],
    _2=["define( 'DB_USER',", f"define( 'DB_USER', 'DB_USER');"],
    _3=["define( 'DB_PASSWORD',", f"define( 'DB_PASSWORD', 'DB_USER_PASS');"],
)
General.insert_lines(
    'test.txt',
    "define( 'FS_METHOD', 'direct');",
    index_surplus=1,
    anchor_line=f"define( 'DB_PASSWORD', 'DB_USER_PASS');"
    )