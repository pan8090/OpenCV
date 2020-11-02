# 写入txt文件
def write(list):
    f = open("a.txt", "a", encoding='utf-8')
    for item in list:  # 每项信息按行存入
        f.write(item)
        f.write('\n')
    f.close()  # 关闭文件


# 读取txt文件
def read():
    f = open("a.txt", "r", encoding='utf-8')
    return f.readlines()  # 按行读取


# 清空txt文件
def clean():
    f = open("a.txt", "r+", enc1oding='utf-8')
    f.truncate()  # 清空文件内容


# 添加员工信息
def add_member():
    id = input("请输入工作id：\n")  # 获取用户输入
    name = input("请输入员工姓名：\n")
    sex = input("请输入性别：\n")
    birthday = input("请输入出生年月：\n")
    address = input("请输入籍贯：\n")
    tel = input("请输入电话：\n")
    # 生成存储有该员工信息的列表
    member = [id, name, sex, birthday, address, tel]
    # 添加到员工信息列表中
    write(member)
    print("添加成功\n")


# 删除员工信息
def dele_member():
    member_list = read()  # 读取存储员工信息的txt文件
    id = input("请输入要删除的员工的工作id：")
    id = id + "\n"  # txt文件内每条信息都以\n结尾，所以为了统一格式，在用户输入的id后也加上\n
    try:
        i = member_list.index(id)  # 获取该id信息在列表中位置，若找不到则会报错 ValueError，所以使用try-except
        for item in range(6):
            member_list.remove(member_list[i])  # 将信息从列表中移除
        clean()  # 清空员工信息txt文件
        write([item[:-1] for item in member_list])  # 将新信息重新写入，写入时将每条数据末尾\n去掉
        print("删除成功")
    except ValueError:  # 报错时提示错误信息
        print("员工不存在")


# 编辑员工信息
def edit_member():
    member_list = read()  # 读取存储员工信息的txt文件
    id = input("请输入需要编辑的员工的工作id：")
    id = id + "\n"  # txt文件内每条信息都以\n结尾，所以为了统一格式，在用户输入的id后也加上\n
    try:
        i = member_list.index(id)  # 获取该id信息在列表中位置，若找不到则会报错 ValueError，所以使用try-except
        member_list[i + 1] = input("请输入员工姓名：\n") + '\n'  # 获取用户输入
        member_list[i + 2] = input("请输入性别：\n") + '\n'
        member_list[i + 3] = input("请输入出生年月：\n") + '\n'
        member_list[i + 4] = input("请输入籍贯：\n") + '\n'
        member_list[i + 5] = input("请输入电话：\n") + '\n'
        clean()  # 清空员工信息txt文件
        write([item[:-1] for item in member_list])  # 将新信息重新写入，写入时将每条数据末尾\n去掉
        print("编辑成功")
    except ValueError:
        print("员工不存在")


# 显示所有员工信息
def show_member():
    member_list = read()  # 读取存储员工信息的txt文件
    member_list = [item[:-1] for item in member_list]  # 将每条数据末尾\n去掉
    for i in range(int(len(member_list) / 6)):  # 每6项为一个员工的信息，所以每6项一输出
        i = i * 6  # 每6项一输出
        print("工作id：", member_list[i], "员工姓名：", member_list[i + 1], "性别：", member_list[i + 2], "出生年月：",  # 输出员工信息
              member_list[i + 3], "籍贯：", member_list[i + 4], "电话：", member_list[i + 5])


# 主方法
def main():
    while True:  # 保证始终进行选择操作
        choice_num = input("请选择:")  # 获取用户输入，判断
        if choice_num == "1":  # 调用添加员工信息函数
            add_member()
        elif choice_num == "2":  # 调用删除员工信息函数
            dele_member()
        elif choice_num == "3":  # 调用编辑员工信息函数
            edit_member()
        elif choice_num == "4":  # 调用显示全部员工信息函数
            show_member()
        elif choice_num == "0":
            print("已退出。")
            return  # 终止主函数
        else:
            print("您的输入有误。")  # 如果输入除了0-4的数，则提示输入有误


# 菜单内容
menu = "员工信息管理系统\n" \
       "1.添加员工信息\n" \
       "2.删除员工信息\n" \
       "3.编辑员工信息\n" \
       "4.查看所有员工信息\n" \
       "0.退出"
# 打印菜单内容
print(menu)
# 运行主方法
main()