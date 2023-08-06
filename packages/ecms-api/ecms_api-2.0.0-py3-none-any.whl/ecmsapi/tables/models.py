from ._base import TableMixin

__all__ = ['HRTEMP', 'HRTCPR', 'PRTMST', 'PRTECN', 'APTCHK', 'APTVEN']

import datetime


class HRTEMP(TableMixin):

    TABLE_NAME = 'HRTEMP'

    HRTEMPID = ('INT', 18)
    STATUSCODE = ('CHAR', 1)
    SRCCNCID = ('INT', 18)
    COMPANYNO = ('DEC', 2)
    DIVISIONNO = ('DEC', 3)
    CHGCNCID = ('INT', 18)
    CHGCOMPANY = ('INT', 2)
    CHGDIVISION = ('DEC', 3)
    EMPCNCID = ('INT', 18)
    EMPCOMPANY = ('DEC', 2)
    EMPDIVISION = ('DEC', 3)
    PRTMSTID = ('INT', 18)
    EMPLOYEENO = ('INT', 9)
    SOCIALSECNO = ('DEC', 9)
    EMPLNAME = ('CHAR', 30)
    ABBRV = ('CHAR', 10)
    ADDR1 = ('CHAR', 30)
    ADDR2 = ('CHAR', 30)
    ADDR3 = ('CHAR', 30)
    CITY = ('CHAR', 20)
    STATECODE = ('CHAR', 2)
    ZIPCODE = ('DEC', 3)
    COUNTRYCODE = ('DEC', 3)
    AREACODE = ('DEC', 3)
    PHONENO = ('DEC', 7)
    CELLPHAC = ('DEC', 3)
    CELLPHNO = ('DEC', 7)
    CONTACTNAME = ('CHAR', 30)
    CONTACTAC = ('DEC', 3)
    CONTACTPHONE = ('DEC', 7)
    BUSUFFIX = ('CHAR', 4)
    CNTRYCODE = ('CHAR', 3)
    MARITALSTAT = ('CHAR', 1)
    LVLCODE = ('DEC', 2)
    OFFICERSCODE = ('CHAR', 1)
    HRTOCCID = ('INT', 18)
    OCCUPDESC1 = ('CHAR', 20)
    OCCUPDESC2 = ('CHAR', 20)
    SEXCODE = ('CHAR', 1)
    MINORITYCODE = ('DEC', 1)
    HANDICAPCODE = ('CHAR', 1)
    DISABLEVEL = ('CHAR', 2)
    BLOODTYPE = ('CHAR', 3)
    BIRTHPLACE = ('CHAR', 25)
    PERMRESIDENT = ('CHAR', 1)
    DRIVERLICNO = ('CHAR', 25)
    DLNUMBER = ('CHAR', 8)
    BIRTHDATE = ('DATE', )
    ORIGHIREDATE = ('DATE', )
    ADJHIREDATE = ('DATE', )
    VACELIGDATE = ('DATE', )
    LASTYEDATE = ('DATE', )
    ELIGSCKACCRL = ('DATE', )
    SICKACRLDATE = ('DATE', )
    EXPRIEDATE = ('DATE', )
    RETIREDDATE = ('DATE', )
    VISAEXPDATE = ('DATE', )
    REVIEWDATE = ('DATE', )
    ESTAVAILDATE = ('DATE', )
    ISSUEI9DATE = ('DATE', )
    I9EXPDATE = ('DATE', )
    ISSUEI9 = ('CHAR', 1)
    COBRALTRDATE = ('DATE', )
    COBRALTRRCVD = ('DATE', )
    COBREASNTFLG = ('CHAR', 1)
    REHIREDATE = ('DATE', )
    HOLELIGDATE = ('DATE', )
    DISABILITYDT = ('DATE', )
    TERMDATE = ('DATE', )
    PRTTRMID = ('INT', 18)
    TERMCODE = ('DEC', 2)
    LASTDAYWK = ('DATE', )
    BENEFITGP = ('CHAR', 50)
    ISSUEAUTH = ('CHAR', 25)
    EVERIFYDT = ('DATE', )
    EVERCASE = ('CHAR', 15)
    EVERCRES = ('CHAR', 25)
    TERMRSN = ('DEC', 3)
    ELGBRHIRE = ('CHAR', 1)
    PRTLBRID = ('INT', 18)
    DEPTNO = ('DEC', 3)
    PRTECLID = ('INT', 18)
    EMPLCLASS = ('DEC', 3)
    EMPLTYPE = ('CHAR', 2)


class HRTCPR(TableMixin):

    TABLE_NAME = 'HRTCPR'
    
    HRTCPRID = ('INT', 18)
    STATUSCODE = ('CHAR', 1)
    SRCCNCID = ('INT', 18)
    COMPANYNO = ('INT', 2)
    DIVISIONNO = ('INT', 3)
    HRTEMPID = ('INT', 18)
    CONTROLNO = ('INT', 20)
    PROPERTYNO = ('INT', 3)
    DESCRIPTION = ('CHAR', 50)
    ASGDATE = ('DATE',)
    RTNDATE = ('DATE',)
    EXPDATE = ('DATE',)
    DUEDATE = ('DATE',)
    RETIREDDATE = ('DATE',)
    APTVENID = ('INT', 18)
    VENDORNO = ('INT', 5)
    PROPAMOUNT = ('INT', 9)
    RETURNEDTO = ('CHAR', 20)
    ADDEDBY = ('CHAR', 20)
    ADDEDDATE = ('TIMESTAMP', 26)
    UPDPGM = ('CHAR', 20)
    UPDATEDBY = ('CHAR', 20)
    UPDDATE = ('TIMESTAMP', 26)

    DEFAULTS = [
            ('STATUSCODE', 'A' ),
            ('SRCCNCID', '5'),
            ('COMPANYNO', '1'),
            ('DIVISIONNO', '0'),
            ('ASGDATE', datetime.date.today()),
            ('UPDPGM', 'HRTP130'),
            ('UPDATEDBY', 'CGCOWNER'),
        ]

    FORIEGN_KEYS = [
        {
            'EMPLOYEENO': {'table': HRTEMP, 'ref': 'HRTEMPID' },
            'OCCUPDESC': {'table': HRTEMP, 'ref': 'OCCUPDESC1'}
        },
    ]


class PRTMST(TableMixin):

    TABLE_NAME = 'PRTMST'

    PRTMSTID = ('INT', 18)
    STATUSCODE = ('CHAR', 18)
    SRCCNCIDCOMPANYNO = ('INT', 18)
    COMPANYNO = ('DEC', 2)
    DIVISIONNO = ('DEC', 3)
    DSTCNCID = ('CHAR', 18)
    DISTCOMPANY = ('DEC', 2)
    DISTDIVISION = ('DEC', 3)
    CSHCNCID = ('INT', 18)
    CSHCOMPANY = ('DEC', 2)
    CSHDIVISION = ('DEC', 3)
    EMPLOYEENO = ('INT', 9)
    EMPNAME = ('CHAR', 18)
    ABBRV = ('CHAR', 18)
    ADDR1 = ('CHAR', 18)
    ADDR2 = ('CHAR', 18)
    ADDR3 = ('CHAR', 18)
    CITY = ('CHAR', 18)
    STATECODE = ('CHAR', 18)
    ZIPCODE = ('CHAR', 18)
    COUNTRYCODE = ('CHAR', 18)
    SYTCCDID = ('INT', 18)
    AREACODE = ('DEC', 18)
    PHONENO = ('DEC', 18)
    CELLPHAC = ('DEC', 18)
    CELLPHNO = ('DEC', 18)
    PAGERAC = ('DEC', 18)
    PAGERNO = ('DEC', 18)
    SOCIALSECNO = ('DEC', 18)
    MARITALSTAT = ('CHAR', 1) #TODO: Finish building class
    OCCUPDESC1 = ('CHAR', 18)
    OCCUPDESC2 = ('CHAR', 18)
    EXEMPTCERTPR = ('CHAR', 18)
    LVLCODE = ('CHAR', 18)
    OFFICERSCODE = ('CHAR', 18)
    SEXCODE = ('CHAR', 18)
    PRTEEIOD = ('CHAR', 18)
    MINOTIRYCODE = ('CHAR', 18)
    BNKMSTID = ('CHAR', 18)
    GLBNKACCT = ('CHAR', 18)
    PAYFREQCDE = ('CHAR', 18)
    PAYTYPE = ('CHAR', 18)
    FEDEXEMPCODE = ('CHAR', 18)
    EXMPTFMSTATE = ('CHAR', 18)
    DECEASEDCODE = ('CHAR', 18)
    PENSIONCODE = ('CHAR', 18)
    PRTUNMID = ('CHAR', 18)
    UNIONNO = ('CHAR', 18)
    BIRTHDATE = ('CHAR', 18)
    ORIGHIREDATE = ('CHAR', 18)
    ADJHIREDATE = ('CHAR', 18)
    BEGININGDATE = ('CHAR', 18)
    LASTWKDATE = ('CHAR', 18)
    TERMDATE = ('CHAR', 18)
    TERMCODE = ('CHAR', 18)
    TERMRSN = ('CHAR', 18)
    ELGBHIRE = ('CHAR', 18)
    HOMESTATE = ('CHAR', 18)
    WCSTATE = ('CHAR', 18)
    PRTSTMID = ('CHAR', 18)
    STIDCODE = ('CHAR', 18)
    FICACODE = ('CHAR', 18)
    FUTACODE = ('CHAR', 18)
    PRTLCMID = ('CHAR', 18)
    LOCALCODE = ('CHAR', 18)
    EXFITAMT = ('CHAR', 18)
    EXFITPCT = ('CHAR', 18)
    OPTTAXCODE = ('CHAR', 18)
    TAXCRCODE = ('CHAR', 18)
    TAXSTATUS = ('CHAR', 18)
    EICSTATUS = ('CHAR', 18)
    FEDDEDAMT = ('CHAR', 18)
    EMPLTIPS = ('CHAR', 18)
    SDIPAYPERCDE = ('CHAR', 18)
    WYNAICSCDE = ('CHAR', 18)
    WYWCCOVERAGE = ('CHAR', 18)
    DEDUCTIONCDE = ('CHAR', 18)
    STDDEPNO = ('CHAR', 18)
    SHIFTNO = ('CHAR', 18)
    PRTECLID = ('CHAR', 18)
    EMPCLASS = ('CHAR', 18)
    EMPTYPE = ('CHAR', 18)
    EMPLGROUP = ('CHAR', 18)
    PRTCRWID = ('CHAR', 18)
    CREWGROUP = ('CHAR', 18)
    CREWNO = ('CHAR', 18)
    JCTMSTID = ('CHAR', 18)
    JOBNO = ('CHAR', 18)
    SUBJOB = ('CHAR', 18)
    COSTCODE = ('CHAR', 18)
    COSTTYPE = ('CHAR', 18)
    STDHOURS = ('CHAR', 18)
    STDCOSTCODE = ('CHAR', 18)
    TICKETNO = ('CHAR', 18)
    FIRSTEMPNAME = ('CHAR', 18)
    MIDDLENAME1 = ('CHAR', 18)
    MIDDLENAME2 = ('CHAR', 18)
    LASTEMPNAME = ('CHAR', 18)
    SUFFIX = ('CHAR', 18)
    SUPERVISOR1 = ('CHAR', 18)

class PRTECN(TableMixin):

    TABLE_NAME = 'PRTECN'

    PRTECNID = ('INT', 18)
    PRTMSTID = ('INT', 18)
    STATUSCODE = ('CHAR', 1)
    COMPANYNO = ('DEC', 2)
    DIVISIONNO = ('DEC', 3)
    EMPLOYEENO = ('INT', 9)
    SEQNO = ('DEC', 2)
    CONTNAME = ('CHAR', 30)
    CELLPHAC = ('DEC', 3)
    CELLPHNO = ('DEC', 7)
    FAXAC = ('DEC', 3)
    FAXPHNO = ('DEC', 7)
    OTHAC = ('DEC', 3)
    OTHPHNO = ('DEC', 7)
    EMAILADDR = ('CHAR', 64)

class APTVEN(TableMixin):

    TABLE_NAME = 'APTVEN'

    STATUSCODE = ('CHAR', 1)
    COMPANYNUMBER = ('DEC', 2)
    DIVISIONNUMBER = ('DEC', 3)
    VENDORNUMBER = ('DEC', 5)
    NAME25 = ('CHAR', 25)

class APTCHK(TableMixin):

    TABLE_NAME = 'APTCHK'

    STATUSCODE = ('CHAR', 1)
    COMPANYNUMBER = ('DEC', 2)
    DIVISIONNUMBER = ('DEC', 3)
    VENDORNUMBER = ('DEC', 5)
    GENLEDGERACCT = ('DEC', 15)
    CHECKNUMBER = ('DEC', 6)
    VENDORNUMBER = ('DEC', 5)
    CHECKAMT = ('DEC', 11)
    CHECKDATE = ('DEC', 8)

    FORIEGN_KEYS = [
        {
            'VENDORNUMBER': {'table': APTVEN, 'ref': 'VENDORNUMBER' },
        },
    ]



