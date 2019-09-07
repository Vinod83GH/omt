from InventoryApp.product_catalogue.models import  *

def process_table_data(result_file_path):
    data_file = open(result_file_path, 'r')
    for count, line in enumerate(data_file):
        if line:
            if line[0].isdigit():
                all_data = line.split()
                split_string= ''
                for data in all_data:
                    if data.isdigit() and (len(data)==4):
                        split_string = data
                        break
                    else:
                        continue
                # if split_string == '':
                #     print("Split string is empty: ",split_string)
                #     index = 0
                #     for data in all_data:
                #         index = index+1
                #         if data.isdigit() and (len(data)==2):
                #             print("condition")
                #             split_string = all_data[index]
                print("split string: ",split_string)
                if split_string != '':
                    new_all_data = line.split(split_string)
                    print(new_all_data)
                    item_name = new_all_data[0].split(' ',1)[1]
                    print('Item Name: ',item_name)
                    other_data = new_all_data[1].split()
                    quantity = other_data[0]
                    print("quantity name: ",quantity)
                    amt = other_data[1]
                    print("Amount: ",amt)
    data_file.close()


