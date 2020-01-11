import pyodbc 

#I downloaded pyodbc it was the library that microsoft said they 'supported',
# but let me know if you want to do it a different way. All the connection
# string info is there. There's a ReadWrite user and a ReadOnly user. I
# currently have the 

conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER={voicelab.database.windows.net,1433};'
    r'DATABASE=db_VoiceLab;'
    # r'UID=sql_services_RW;'
    # r'PWD=c!5c0p5Dt!;'
    r'UID=sql_services_RO;'
    r'PWD=c!5c0p5Dt!;'
    )

cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()

#Sample select query
# cursor.execute("SELECT @@version;") 
# row = cursor.fetchone() 
# while row: 
#     print(row[0])
#     row = cursor.fetchone()

# This one pulls data out of our Carrier table. These 3 rows are every
# bit of data I have in the DB right now.
cursor.execute("SELECT * FROM tblCarriers;") 
row = cursor.fetchone() 
while row:
    print(row[0],row[1],row[2])
    row = cursor.fetchone()