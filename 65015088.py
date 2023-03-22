import matplotlib.pyplot as plt
from pandas import DataFrame
from requests import get
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import *



#สร้าตัวแปรไว้เก็บค่าเปอร์เซ็นของ pieที่ 2
valueforpie2 = []
#สร้าตัวแปรไว้เก็บค่าเปอร์เซ็นของ pieที่ 3
valueforpie3 = []
#สร้าตัวแปรไว้เก็บค่าเปอร์เซ็นของ pieที่ 4
valueforpie4 = []
#สร้าตัวแปรไว้เก็บค่าเปอร์เซ็นของ pieที่ 5
valueforpie5 = []
#สร้าตัวแปรไว้เก็บค่าของชื่อวิทยาศาสตร์ทั้งหมดa
forcomboboxsc = []
#สร้าตัวแปรไว้เก็บค่าของชื่อไทยทั้งหมด
forcomboboxth = []
#สร้างตัวแปรมาเก็บข้อมูล วงศ์
forwong = []
#try reaquest ข้อมูลจาก data go
try:
    #user token สำหรับใช้ผ่าน Data go
    api_key = "aVxKbRLaOGUo9lEPxzhVWQIHaHKIdruQ"
    headers = {
        "api-key": api_key,
    }

    #resource_id ไว้ใช้หาข้อมูลที่ต้องการตั้ง limit ไว้ที่ 2000 
    params = {"resource_id": "c789e1be-ab06-43dd-93fa-80e55f6b44ac", "limit": 2000}
    #requests ไปที่ data go
    r = get(
        "https://opend.data.go.th/get-ckan/datastore_search", params, headers=headers
    )
#เรียกไม่สำเร็จให้แสดงข้อความไม่สามารถเชื่อมต่อได้
except:
    print("ไม่สามารถเชื่อมต่อกับ API ลองใหม่อีกครั้ง")
    exit()
#ถ้า requests สำเร็จ
if r.ok:
    try:
        j = r.json()
        records = j["result"]["records"]
    except:
        print("ไม่สามารถเชื่อมต่อกับ API ลองใหม่อีกครั้ง")
        exit()

    
#กำหนด font ของการ plot grah
plt.rcParams['font.family']='Tahoma'

#สร้าง data frame จาก pandas และลบช่องว่างออก ข้อมูลมีการใส่ผิดเช่น เว้นช่องว่างทำให้มีหัวข้อเดิมซ้ำมา
df = DataFrame(records).replace(' ', '', regex=True).replace("VU","มีแนวโน้มใกล้สูญพันธุ์").replace("EX","สูญพันธุ์").replace("EW","สูญพันธุ์ในธรรมชาติ").replace("EN","ใกล้สูญพันธุ์").replace("NT","ใกล้ถูกคุกคาม").replace("LC","เป็นกังวลน้อยที่สุด").replace("R","หายากระดับโลก").replace("RT","หายาก(ประเทศไทย)").replace("CR","ใกล้สูญพันธุ์อย่างยิ่ง").replace("(CR)","หายากระดับโลกปี 1994").replace("(EN)","หายากระดับโลกปี 1994").replace("(VU)","หายากระดับโลกปี 1994").replace("(NT)","หายากระดับโลกปี 1994").replace("LC(VU)","เป็นกังวลน้อยที่สุด").replace("VUCR","ใกล้สูญพันธุ์อย่างยิ่ง")
#สร้าง data frame จาก pandas ที่มีช่องว่างเพื่อให้ตรงกับชื่อวิทยาศาสตร์ของข้อมูลโดยตัดตัวอักษรพิเศษทิ้งทั้งหมดยกเว้น spacebar และ วรรณยุกต์ไทย
dfforfind = DataFrame(records).replace(r'[^\w\s้่๋็ะัํ๊ีฯุูึำัีืิ์่]', '', regex=True).replace("VU","มีแนวโน้มใกล้สูญพันธุ์").replace("EX","สูญพันธุ์").replace("EW","สูญพันธุ์ในธรรมชาติ").replace("EN","ใกล้สูญพันธุ์").replace("NT","ใกล้ถูกคุกคาม").replace("LC","เป็นกังวลน้อยที่สุด").replace("R","หายากระดับโลก").replace("RT","หายาก(ประเทศไทย)").replace("CR","ใกล้สูญพันธุ์อย่างยิ่ง").replace("(CR)","หายากระดับโลกปี 1994").replace("(EN)","หายากระดับโลกปี 1994").replace("(VU)","หายากระดับโลกปี 1994").replace("(NT)","หายากระดับโลกปี 1994").replace("LC(VU)","เป็นกังวลน้อยที่สุด").replace("VUCR","ใกล้สูญพันธุ์อย่างยิ่ง")

#ใส่ข้อมูลเข้าไปใน list เพื่อใช้ใน combobox ค้นหาด้วยตัวเลือก
for i in dfforfind['ชื่อวิทยาศาสตร์']:
    forcomboboxsc.append(i)
for i in dfforfind['ชื่อไทย']:
    if i.isalpha():
        forcomboboxth.append(i)
for i in set(dfforfind['วงศ์']):
    forwong.append(i)
forcomboboxsc.sort()
forcomboboxth.sort()
forwong.sort()


root = Tk()
#กำหนด font ของ tkinter
root.option_add('*font', ('verdana', 12, 'bold'))
root.title("พืชที่ถูกคุกคามในประเทศไทย")
root.configure(bg='#856ff8')
def countofplant():
    plt.close()
    #กำหนด size หน้าจอ
    px = 1/plt.rcParams['figure.dpi']
    plt.subplots(figsize=(1200*px,800*px))
    #จัดข้อมูลให้อยู่ในรูปที่มีแต่หัวข้อของกลุ่มของพืช และ จำนวนกลุ่มของพืช
    countofplantdf = df['กลุ่มของพืช'].value_counts().rename_axis('sub_value').reset_index(name='count_value')
    #สร้างตัวแปรมาเก็บข้อมูล countofplantdf ในหัวข้อ sub_value
    countofplantlabel = countofplantdf.sub_value
     #สร้างตัวแปรมาเก็บข้อมูล countofplantdf ในหัวข้อ count_value
    countofplantcount = countofplantdf.count_value
    #กำหนดให้มี row เดียว 2 column และอยู่ตำแหน่งที่ 1
    plt.subplot(1,2,1)
    #กำหนด title ของ กราฟเป็น จำนวนกลุ่มของพืช
    plt.title('จำนวนกลุ่มของพืช')
    #สร้าง bar กราฟจาก dataframe
    countofplant = plt.barh(countofplantlabel, countofplantcount, color= 'maroon')
    #นำ value ของ countofplantcount ไปที่บน bar กราฟ
    plt.bar_label(countofplant,labels=countofplantcount,fontsize=9)
    #กำหนดให้มี row เดียว 2 column และอยู่ตำแหน่งที่ 2      
    plt.subplot(1,2,2)
    plt.title('ประเภทของกลุ่มของพืช')
    #สร้าง pie กราฟจาก countofplantcount labels เป็น countofplantlabel และใช้ autopct เพื่อสร้างเปอร์เซ็นต์ในกราฟ 
    plt.pie(countofplantcount,labels=countofplantlabel,autopct='%1.2f%%')
    #show กราฟ
    plt.show()
def status1():
    plt.close()
    #กำหนด size หน้าจอ
    px = 1/plt.rcParams['figure.dpi']
    plt.subplots(figsize=(1200*px,800*px))
    #จัดข้อมูลให้อยู่ในรูปที่มีแต่หัวข้อของสถานภาพ ก่อน ค.ศ. 1994
    status1beforedf = df['สถานภาพ (ก่อน ค.ศ. 1994)'].value_counts().rename_axis('sub_value').reset_index(name='count_value')
    #สร้างตัวแปรมาเก็บข้อมูล status1beforedf ในหัวข้อ sub_value
    status1dfbeforelabel = status1beforedf.sub_value
    #สร้างตัวแปรมาเก็บข้อมูล status1beforedf ในหัวข้อ count_value
    status1dfbeforecount = status1beforedf.count_value
    #กำหนดให้มี row 2  2 column และอยู่ตำแหน่งที่ 1
    plt.subplot(2,2,1)
    plt.title('จำนวนสถานภาพในช่วงก่อน ค.ศ. 1994')
    #ใช้ plot กราฟ bar ของ pandas
    statusbefore = plt.barh(status1dfbeforelabel, status1dfbeforecount, color= 'maroon')
    #นำ value ของ status1dfbeforecount ไปที่บน bar กราฟ
    plt.bar_label(statusbefore,labels=status1dfbeforecount,fontsize=9)
    #เรียกข้อมูลจาก status1dfbeforecount และใส่เข้าไปใน valueforpie2
    for index, value in enumerate(status1dfbeforecount):
         value = (value/len(df))*100
         valueforpie2.append(float(f"{value:.1f}"))
    #กำหนดให้มี row 2  2 column และอยู่ตำแหน่งที่ 2      
    plt.subplot(2,2,2)
    #title สภานภาพ (ก่อน ค.ศ. 1994)
    plt.title('สถานภาพ (ก่อน ค.ศ. 1994)')
    #pie ใช้ค่าจาก status1dfcount ซึ่งเก็บค่ามาจาก สถานภาพ (ก่อน ค.ศ. 1994)
    plt.pie(status1dfbeforecount)
    #ใช้ตัวแปร labels เก็บ หัวข้อ และ value
    labels = [f'{l}, {s:0.1f}%' for l, s in zip(status1dfbeforelabel,valueforpie2)]
    #plot legend ออกมาด้วย ค่าจาก pie ที่ 2 และ labels คือ หัวข้อ และ value ที่เก็บมา
    plt.legend(status1dfbeforelabel, labels=labels,bbox_to_anchor=(1,1))

    #จัดข้อมูลให้อยู่ในรูปที่มีแต่หัวข้อของสถานภาพ (ในช่วง ค.ศ. 1994-2001)
    status1afterdf = df['สถานภาพ (ในช่วง ค.ศ. 1994-2001)'].value_counts().rename_axis('sub_value').reset_index(name='count_value')
    #สร้างตัวแปรมาเก็บข้อมูล status1afterdf ในหัวข้อ  sub_values
    status1afterdflabel = status1afterdf.sub_value
    #สร้างตัวแปรมาเก็บข้อมูล status1afterdf ในหัวข้อ count_value
    status1afterdfcount = status1afterdf.count_value
    #กำหนดให้มี row 2  2 column และอยู่ตำแหน่งที่ 3
    plt.subplot(2,2,3)
    plt.title('จำนวนสถานภาพในช่วง ค.ศ. 1994-2001')
    statusafter = plt.barh(status1afterdflabel, status1afterdfcount, color= 'blue')
    #นำ value ของ status1afterdfcount ไปที่บน bar กราฟ
    plt.bar_label(statusafter,labels=status1afterdfcount,fontsize=9)
    for index, value in enumerate(status1afterdfcount):
         value2 = (value/len(df))*100
         valueforpie3.append(float(f"{value2:.1f}"))
    #กำหนดให้มี row 2  2 column และอยู่ตำแหน่งที่ 4      
    plt.subplot(2,2,4)
    plt.title('สถานภาพ (ในช่วง ค.ศ. 1994-2001)')
    plt.pie(status1afterdfcount)
    labels2 = [f'{l}, {s:0.1f}%' for l, s in zip(status1afterdflabel,valueforpie3)]
    plt.legend(status1afterdfcount, labels=labels2,bbox_to_anchor=(1,1))
    plt.show()
def shape():
    plt.close()
    #กำหนด size หน้าจอ
    px = 1/plt.rcParams['figure.dpi']
    plt.subplots(figsize=(1200*px,800*px))
    shapedf = df['ลักษณะวิสัย'].value_counts().rename_axis('sub_value').reset_index(name='count_value')
    shapedflabel = shapedf.sub_value
    shapedfcount = shapedf.count_value
    #กำหนดให้มี row 2 row 2 column และอยู่ตำแหน่งที่ 1
    plt.subplot(2,2,1)
    plt.title("จำนวนลักษณะวิสัย")
    plt.xticks(rotation = 90,fontsize=9)
    barplot = plt.bar(shapedflabel, shapedfcount,color= 'blue')
    plt.bar_label(barplot,labels=shapedfcount,fontsize=6)

    for index, value in enumerate(shapedfcount):
         value= (value/len(df))*100
         valueforpie4.append(float(f"{value:.1f}"))
    #กำหนดให้มี row 2 row 2 column และอยู่ตำแหน่งที่ 2      
    plt.subplot(2,2,2)
    #title ลักษณะวิสัย
    plt.title('ลักษณะวิสัย')
    #pie ใช้ค่าจาก forpie2 ซึ่งเก็บค่ามาจากลักษณะวิสัย
    plt.pie(shapedfcount)
    #ใช้ตัวแปร labels เก็บ หัวข้อ และ value
    labels = [f'{l}, {s:0.1f}%' for l, s in zip(shapedflabel,valueforpie4)]
    #plot legend ออกมาด้วย ค่าจาก pie ที่ 2 และ labels คือ หัวข้อ และ value ที่เก็บมา
    plt.legend(shapedfcount, labels=labels,prop={'size': 6},bbox_to_anchor=(1,1))
    plt.show()
def wong():
    plt.close()
    #ทำ dataframe จาก column 4,8 และ 9
    df1 = dfforfind.iloc[:, [4,8,9]]
    find_get = sub4.get()
    pievalue = []
    pielabel = []
    if find_get:
            #ใช้ dataframe ที่ทำค้นหาชื่อ
            rowname = df1[df1['วงศ์'].str.contains(find_get)]
            #สร้าตัวแปรไว้สำหรับการหาค่าใน column สถานภาพ (ในช่วง ค.ศ. 1994-2001)
            vu = rowname[rowname['สถานภาพ (ในช่วง ค.ศ. 1994-2001)']=='มีแนวโน้มใกล้สูญพันธุ์'].count().reset_index(name='count_value')
            vulabelcount = list(vu.count_value)
            vu2 = rowname[rowname['สถานภาพ (ในช่วง ค.ศ. 1994-2001)']=='สูญพันธ์ุในธรรมชาติ'].count().reset_index(name='count_value')
            vulabelcount2 = list(vu2.count_value)
            vu3 = rowname[rowname['สถานภาพ (ในช่วง ค.ศ. 1994-2001)']=='ใกล้สูญพันธุ์อย่างยิ่ง'].count().reset_index(name='count_value')
            vulabelcount3 = list(vu3.count_value)
            vu4 = rowname[rowname['สถานภาพ (ในช่วง ค.ศ. 1994-2001)']=='ใกล้สูญพันธุ์'].count().reset_index(name='count_value')
            vulabelcount4 = list(vu4.count_value)
            vu6 = rowname[rowname['สถานภาพ (ในช่วง ค.ศ. 1994-2001)']=='ใกล้ถูกคุกคาม'].count().reset_index(name='count_value')
            vulabelcount6 = list(vu6.count_value)
            vu7 = rowname[rowname['สถานภาพ (ในช่วง ค.ศ. 1994-2001)']=='เป็นกังวลน้อยที่สุด'].count().reset_index(name='count_value')
            vulabelcount7 = list(vu7.count_value)
            vu8 = rowname[rowname['สถานภาพ (ก่อน ค.ศ. 1994)']=='หายากระดับโลก'].count().reset_index(name='count_value')
            vulabelcount8 = list(vu8.count_value)
            vu9 = rowname[rowname['สถานภาพ (ก่อน ค.ศ. 1994)']=='หายาก(ประเทศไทย)'].count().reset_index(name='count_value')
            vulabelcount9 = list(vu9.count_value)
            vu10 = rowname[rowname['สถานภาพ (ในช่วง ค.ศ. 1994-2001)']=='หายากระดับโลกปี 1994'].count().reset_index(name='count_value')
            vulabelcount10 = list(vu10.count_value)
            #เช็คว่าค่าเป็น 0 หรือไม่
            if int(vulabelcount[0]) > 0:
                pievalue.append(vulabelcount[0])
                pielabel.append('มีแนวโน้มใกล้สูญพันธุ์')
            if int(vulabelcount2[0]) > 0:
                pievalue.append(vulabelcount2[0])
                pielabel.append('สูญพันธ์ุในธรรมชาติ')
            if int(vulabelcount3[0]) > 0:
                pievalue.append(vulabelcount3[0])
                pielabel.append('ใกล้สูญพันธุ์อย่างยิ่ง')
            if int(vulabelcount4[0]) > 0:
                pievalue.append(vulabelcount4[0])
                pielabel.append('ใกล้สูญพันธุ์')
            if int(vulabelcount6[0]) > 0:
                pievalue.append(vulabelcount6[0])
                pielabel.append('ใกล้ถูกคุกคาม')
            if int(vulabelcount7[0]) > 0:
                pievalue.append(vulabelcount7[0])
                pielabel.append('เป็นกังวลน้อยที่สุด')
            if int(vulabelcount8[0]) > 0:
                pievalue.append(vulabelcount8[0])
                pielabel.append('หายากระดับโลก')
            if int(vulabelcount9[0]) > 0:
                pievalue.append(vulabelcount9[0])
                pielabel.append('หายาก(ประเทศไทย)')
            if int(vulabelcount10[0]) > 0:
                pievalue.append(vulabelcount10[0])
                pielabel.append('หายากระดับโลกปี 1994')
            
            plt.title(f"วงศ์ {find_get} มีจำนวน {len(rowname)}")
            #zip pielabel กับ pievalue ไว้ด้วยกัน
            labels = [f'{l}, {s}' for l, s in zip(pielabel,pievalue)]
            plt.pie(pievalue,labels=labels)
   
            plt.show()
  
    else:
        messagebox.showinfo("ALERT", "กรุณาป้อนข้อมูล")


def find_plant_EN():
    f = ""
    #รับค่ามาจาก sub2 หรือช่องชื่อวิทยาศาสตร์
    find_get = sub2.get()
    if find_get:
            rowname = dfforfind[dfforfind['ชื่อวิทยาศาสตร์'].str.contains(find_get)]
            for key,value in rowname.iterrows():
                    f += str(value)
            messagebox.showinfo("DATA", f)
    else:
        messagebox.showinfo("ALERT", "กรุณาป้อนข้อมูล")
def find_plant_TH():
    f = ""
    find_get = sub3.get()
    if find_get:
            rowname = df[df['ชื่อไทย'].str.contains(find_get)]
            for key,value in rowname.iterrows():
                    f += str(value)
            messagebox.showinfo("DATA", f)
    else:
        messagebox.showinfo("ALERT", "กรุณาป้อนข้อมูล")
    
def send():
    #สร้างตัวแปรเก็บค่ามาจาก combobox
    get = sub.get()
    if get == 'ประเภทของกลุ่มของพืช':
        countofplant()
    elif get == 'สถานภาพ':
        status1()
    elif get == 'ลักษณะวิสัย':
        shape()
    else:
        messagebox.showinfo("ALERT", "ข้อมูลไม่ถูกต้อง")

Label(root, text="overview").grid(column=0, row=0,padx=10,pady=10)
#บอกจำนวนข้อมูลทั้งหมด
Label(root, text=f"ข้อมูลทั้งหมด : {len(df)} จำนวน").grid(column=1, row=0,padx=10,pady=10)
#COMBOBOX
sub = Combobox(root, width = 15, justify="right")
sub['values'] = (              
                                'ประเภทของกลุ่มของพืช',
                                'สถานภาพ',
                                'ลักษณะวิสัย')


#กำหนดค่าเริ่มต้นของ COMBOBOX เป็น overview
sub.set("ประเภทของกลุ่มของพืช")
#โชว์ COMBOBOX
sub1 = sub.grid(column=0, row=1,padx=10,pady=10)
#ปุ่มกดตกลง
send = Button(text="ตกลง",command=send).grid(column = 1, row=1 ,padx=20,pady=10)


#sub4 คือ combobox ของ วงศ์
sub4 = Combobox(root, width = 15, justify="right")
sub4['values'] = forwong
sub4.set("ชื่อวงศ์")
sub4_ = sub4.grid(column=0, row=6,padx=10,pady=10)
wonggraph = Button(text="ตกลง",command=wong).grid(column = 1, row=6 ,padx=20,pady=10)

Label(root, text="เลือกหรือพิมพ์เพื่อค้นหารายละเอียด").grid(column=0, row=7,padx=10,pady=10)
#sub3 คือ combobox ของชื่อไทย
sub3 = Combobox(root, width = 15, justify="right")
sub3['values'] = forcomboboxth
sub3.set("ชื่อไทย")
sub3_ = sub3.grid(column=0, row=8,padx=10,pady=10)
find_EN2 = Button(text="ค้นหา",command=find_plant_TH).grid(column = 1, row=8 ,padx=20,pady=10)

#sub2 คือ combobox ของชื่อวิทยาศาสตร์
sub2 = Combobox(root, width = 15, justify="right")
sub2['values'] = forcomboboxsc
sub2.set("ชื่อวิทยาศาสตร์")
sub2_ = sub2.grid(column=0, row=9,padx=10,pady=10)
find_EN2 = Button(text="ค้นหา",command=find_plant_EN).grid(column = 1, row=9 ,padx=20,pady=10)


root.mainloop()