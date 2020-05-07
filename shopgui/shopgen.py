# -*- coding: utf-8 -*-

# shop generator
# execute in BDS/BDX root dir

import os, shutil, json

BDS_CHECK_FILE = 'bedrock_server.exe'
SHOP_TEMPLATE = 'shop_tpl.json'

SHOP_LUA_TPL = '''function u_shop(name)
    GUI(name, "u_shop")
end


function generic_item(name, raw, data, item, subid, price1, price2)
    local number = raw[2]
    if raw[1] == 0 then
        local price1_total = number * price1
        if rdMoney(name, price1_total) then
            --invapi.giveItem(name, item, number, subid)
            runCmd(string.format('give %s %s %i %i', name, item, number, subid))
            Log("BUY", name, item, subid, price1, number, price1_total)
            sendText(name, "§aВы приобрели товар и потратили §l§6" .. price1_total .. " ")
            GUI(name, "u_shop")
            return
        else
            sendText(name, "§cНе хватает денег.")
            return
        end
    end
    if raw[1] == 1 then
        local price2_total = number * price2
        if safe_clear(name, string.format("%s %i", item, subid), number) then
            addMoney(name, price2_total)
            Log("SELL", name, item, subid, price2, number, price2_total)
            sendText(name, "§aВы продали товар и заработали §l§6" .. price2_total .. " ")
            GUI(name, "u_shop")
            return
        else
            sendText(name, "§cНедостаточно вещей для продажи.")
            return
        end
    end
end

'''

def detect_bds():
    if os.path.exists(BDS_CHECK_FILE) and os.path.exists('gui') and os.path.exists('lua'):
        return True
    else:
        return False

def del_file(path):
    if os.path.exists(path):
        os.remove(path)

def del_dir(path):
    if os.path.exists(path):
        shutil.rmtree("gui/shop_gui")

def clean_old_files():
    del_dir("gui/shop_gui")
    del_file("gui/u_shop")
    del_file("lua/shop.lua")

def load_json():
    with open(SHOP_TEMPLATE, encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data

def write_file(filename, text):
    with open(filename, 'w', encoding="utf-8") as txtfile:
        txtfile.write(text)


def main():
    main_gui = 'type=simple, cb=shop, title=§8Магазин\n'
    main_lua = 'function shop(name, selected, text)\n'
    sublists_lua = ''
    itemfuncs_lua = ''

    # check if we are in bds/bdx directory
    if not detect_bds():
        print("This script need to be run from BDS/BDX root dir.")
        return -1
    print("Ok, we are in main BDS/BDX dir...")
    print("Searching for shop template json...")
    if not os.path.exists(SHOP_TEMPLATE):
        print("Shop template json file not found :( Exiting.")
        return -1
    print("Ok, template is here. Should I process and recreate shop lua and GUI files?")
    print("WARNING! All existing shop files will be deleted and replaced with the new ones!")
    print("Enter OK (uppercase) to confirm or anything else to cancel:")
    if not input() == 'OK':
        print('Script was canceled. No files were changed or deleted.')
        return
    print("Deleting old files (gui/shop, gui/shop_gui dir, lua/shop.lua)...")
    clean_old_files()
    print("Loading json schema...")
    json_tpl = load_json()
    print('Creating files...')
    os.mkdir('gui/shop_gui')
    for i, menuitem in enumerate(json_tpl):
        main_gui += f"text=§8{menuitem['title']}, img=textures/{menuitem['image']}\n"
        main_lua += f"if selected == {i} then\n GUI(name, \"shop_gui/list_{menuitem['id']}\", getMoney(name))\n return\n end\n"
        sublist_lua = f"function list_{menuitem['id']}(name, selected, text)\n"
        sublist_gui = f"type=simple, cb=list_{menuitem['id']}, title={menuitem['title']}, content=§eВаши деньги - %1§f\\nКупить | Продать\n"
        for j, item in enumerate(menuitem['items']):
            sublist_lua += f"if selected == {j} then\n GUI(name, \"shop_gui/{item['item_name']}_{item['aux_id']}\", getMoney(name))\n return\n end\n"
            itemfuncs_lua += f"function {item['item_name']}_{item['aux_id']}(name, raw, data)\n" \
                             f"    generic_item(name, raw, data, \"{item['item_name']}\", {item['aux_id']}, {item['buy_price']}, {item['sell_price']})\nend\n\n"
            sublist_gui += f"text={item['title']}. Куп:{item['buy_price']} | Прод:{item['sell_price']}, img=textures/{item['image']}\n"

            item_page = f"type=full, cb={item['item_name']}_{item['aux_id']}, cb2=u_shop, title={item['title']}. Куп: {item['buy_price']}  | Прод: {item['sell_price']} , content=§3Ваши деньги - %%1§1\n" \
                'type=dropdown,text=Действие,args=["Купить","Продать"]\n' \
                    f"type=slider,text=Количество,min=1,max=64,def={item['default_amount']}"
            write_file(f"gui/shop_gui/{item['item_name']}_{item['aux_id']}", item_page)
        sublist_gui += 'text=Назад, img=textures/ui/icon_import'
        write_file(f"gui/shop_gui/list_{menuitem['id']}", sublist_gui)
        sublist_lua += 'GUI(name, "u_shop")\nend\n\n'
        sublists_lua += sublist_lua

    main_lua += 'end\n\n'
    write_file('gui/u_shop', main_gui)
    write_file('lua/shop.lua', SHOP_LUA_TPL + main_lua + sublists_lua + itemfuncs_lua)
    print("Shop files were generated successfully!")
    print("Do \"/gui shop\" command to open shop main GUI.")

if __name__ == "__main__":
    main()
