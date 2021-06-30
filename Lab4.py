import pyodbc
# Some other example server values are
server = 'LAPTOP-KC0GUUBK' # for a named instance
# server = 'myserver,port' # to specify an alternate port
# server = 'tcp:myserver.database.windows.net' 
database = 'Lab3' 
cnxn = pyodbc.connect('DRIVER={SQL Server}; SERVER='+server+'; DATABASE='+database+'; Trusted_Connection=yes;')
cursor = cnxn.cursor()

# Gets the names of all tables in the database
tables = []
for tableName in cursor.tables():
    tables.append(tableName.table_name)

def addData(table):
    if table not in tables:
        print("Table does not exist in this database")
        return
    values = []

    #4 int, -9 date, 12 varchar, 6 is float
    values = []
    for row in cursor.columns(table):
        columnDataType = row.data_type
        if columnDataType == 4 or columnDataType == 6:
            values.append(input("Please enter the value for " + row.column_name + " "))
        else:
            values.append("'"+input("Please enter the value for " + row.column_name + " ")+"'")

    addQuery = "INSERT INTO "+table+" values ( "
    for value in values:
        addQuery += value
        if value != values[-1]:
            addQuery += ", "
    addQuery += ' )'
    try:
        cursor.execute(addQuery)
    except:
        print("Error could not add the values")
        print("Check if the data types are correct, Syntax for date is yyyy-mm-dd")
        return

def removeData(table):
    if table not in tables:
        print("Table does not exist in this database")
        return
    
    columnNames = []
    for row in cursor.columns(table):
        columnNames.append(row.column_name)

    print("The table "+table+" has these columns ")
    print(columnNames)
    condition = input("Please input the condition of the remove such as name='George' ")
    removeQuery = "delete from "+table+" where "+condition
    try:
        cursor.execute(removeQuery)
    except:
        print("Error the condition is invalid")
        return

def viewData(table):
    if table not in tables:
        print("Table does not exist in this database")
        return
    
    columnNamesCheck = ['q']
    columnNames = []
    for row in cursor.columns(table):
        columnNames.append(row.column_name)
        columnNamesCheck.append(row.column_name)

    viewQuery = "select "
    column=''
    chosenColumns = []
    while True:
        while column not in columnNamesCheck:
            print("This table has these columns ")
            print(columnNames)
            column = input("Input the name of the column you want to see and type q to quit ")
            if column not in columnNames:
                print("Column not in table")
        if column.lower() == 'q':
            viewQuery = viewQuery[:-1]
            break
        viewQuery += column + ','
        chosenColumns.append(column)
        column = ''

    if chosenColumns == []:
        viewQuery += "*"
        chosenColumns = columnNames
    
    viewQuery += " from "+table
    cursor.execute(viewQuery)
    print(chosenColumns)
    row = cursor.fetchone()
    while row:
        print(row)
        row = cursor.fetchone()

def selectData(table):
    if table not in tables:
        print("Table does not exist in this database")
        return
    
    columnNamesCheck = ['q']
    columnNames = []
    for row in cursor.columns(table):
        columnNames.append(row.column_name)
        columnNamesCheck.append(row.column_name)

    viewQuery = "select "
    column=''
    chosenColumns = []
    while True:
        while column not in columnNamesCheck:
            print("This table has these columns ")
            print(columnNames)
            column = input("Input the name of the column you want to see and type q to quit ")
            if column not in columnNames:
                print("Column not in table")
        if column.lower() == 'q':
            viewQuery = viewQuery[:-1]
            break
        viewQuery += column + ','
        chosenColumns.append(column)
        column = ''

    if chosenColumns == []:
        viewQuery += "*"
        chosenColumns = columnNames
    
    viewQuery += " from "+table
    print("The table "+table+" has these columns ")
    print(columnNames)
    condition = input("Please input the condition of the remove such as name='George' ")
    viewQuery += " where "+condition

    try:
        cursor.execute(viewQuery)
    except:
        print("Error the condition is invalid")
        return
    
    print(chosenColumns)
    row = cursor.fetchone()
    while row:
        print(row)
        row = cursor.fetchone()

def customData():
    while True:
        query = input("Please input your custom queries type q to quit ")
        if query.lower() == 'q':
            return
        try:
            cursor.execute(query)
        except:
            print("Error query was not able to be run")
    
queryFunctions = ['add', 'remove', 'view', 'select', 'custom', 'q']
query = ""
while True:
    while query.lower() not in queryFunctions:
        query = input("Type add, remove, view, select, custom, or q to quit.\n")
        query = query.lower()
    if query == "q":
        break
    if query == "add":
        tableName = input("Please input the table you would like to add data to ")
        addData(tableName)
    if query == "remove":
        tableName = input("Please input the table you would like to remove data from ")
        removeData(tableName)
    if query == "view":
        tableName = input("Please input the table you would like to view data from ")
        viewData(tableName)
    if query == "select":
        tableName = input("Please input the table you would like to select data from ")
        selectData(tableName)
    if query == "custom":
        customData()
    query = ''
