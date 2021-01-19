# sql = "SELECT * FROM \"%s\" WHERE %s = ?" % ( self.table,  self.fid_col)

# sql = """
# SELECT
#     title,
#     first_name,
#     last_name,
#     suffix,
#     occupation,
#     employer,
#     address1,
#     address2,
#     city,
#     state,
#     zipcode,
#     committee_id,
#     COUNT(*)
# FROM (
#     SELECT
#         ctrib_namt as title,
#         ctrib_namf as first_name,
#         ctrib_naml as last_name,
#         ctrib_nams as suffix,
#         ctrib_occ as occupation,
#         ctrib_emp as employer,
#         ctrib_adr1 as address1,
#         ctrib_adr2 as address2,
#         ctrib_city as city,
#         ctrib_st as state,
#         ctrib_zip4 as zipcode,
#         cmte_id as committee_id
#     FROM %(rcpt)s

#     UNION ALL

#     SELECT
#         lndr_namt as title,
#         lndr_namf as first_name,
#         lndr_naml as last_name,
#         lndr_nams as suffix,
#         loan_occ as occupation,
#         loan_emp as employer,
#         loan_adr1 as address1,
#         loan_adr2 as address2,
#         loan_city as city,
#         loan_st as state,
#         loan_zip4 as zipcode,
#         cmte_id as committee_id
#     FROM %(loan)s

#     UNION ALL

#     SELECT
#         enty_namt as title,
#         enty_namf as first_name,
#         enty_naml as last_name,
#         enty_nams as suffix,
#         ctrib_occ as occupation,
#         ctrib_emp as employer,
#         '' as address1,
#         '' as address2,
#         enty_city as city,
#         enty_st as state,
#         enty_zip4 as zipcode,
#         cmte_id as committee_id
#     FROM %(s497)s
# ) as t
# GROUP BY
#     title,
#     first_name,
#     last_name,
#     suffix,
#     occupation,
#     employer,
#     address1,
#     address2,
#     city,
#     state,
#     zipcode,
#     committee_id
# ORDER BY
#     last_name,
#     first_name,
#     suffix,
#     title,
#     city,
#     state,
#     occupation,
#     employer
# """ % dict(
#     rcpt=models.RcptCd._meta.db_table,
#     loan=models.LoanCd._meta.db_table,
#     s497=models.S497Cd._meta.db_table,
# )

context['related_url'] = mark_safe(related_url)
# f.context = mark_safe(related_url)

# x = int(input())
# x = str(input())
# x = float(input())
# x = 'input'
# y = input()


# def getRoll(name):
#     return 931

# x = getRoll('')


# username = 'ashsjhdk'
# password = 'sdushdiushd'
# x = 2
# name = "Miran Al " + "Mehrab"

# roll = getRoll('Miran')


# self.abc = 'abc'
# x = self.abc

# s = socket.socket.socket(AF.NET, AF.Packet)


# x = y = z = "Orange"
# x, y, z = "Orange", "Banana", "Cherry"


# x = ['apple','oneplus','pinephone']

# x = {"brand":'apple',"model": "se 2020", "upass": "", name: 'jkahhjdv'}
# tokens = ['sahzslkdjl3434sdasd','dsdlsahkljah746548','sdlshkqj2232324','2323dsafnsdfjkn']

# admin = 'admin'

# x = ('root', 'name', 'password', abhsd)
# y = {'root', 'name', 'password', itwqughdf}



# header[authorization] = "bearer:"+token
# header[0] = 'sdfsd'

# token = 'saldhiu322uh2i3278siabcxhabxgsua'


