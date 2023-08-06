from ecmsapi.tables._base import TableMixin, DbTypes

TABLE_PREFIX = 'GLT'
AVAILABLE_TABLES = ['MST', 'PST', 'ROW', 'ACT', 'FRN']

__all__ = list(map(lambda x: f'{TABLE_PREFIX}{x}', AVAILABLE_TABLES))

class GLTMST(TableMixin):

    TABLE_NAME = 'GLTMST'

    GLTMSTID = DbTypes.INT(1)
    STATUSCODE = DbTypes.CHAR(20)
    SRCCNCID = DbTypes.INT()
    COMPANYNO = DbTypes.INT()
    DIVISIONNO = DbTypes.INT()
    GLACCTNO = DbTypes.CHAR(16, 'GL Account')
    DESCRIPTION = DbTypes.CHAR(25)
    DBCRCODE = DbTypes.INT()
    GLTACCTTYPE = DbTypes.INT()
    FINSTMTTYPE = DbTypes.INT()
    GLAPPLCODE = DbTypes.INT(1)
    LASTMAINTDT = DbTypes.TIMESTAMP()
    ALTGLACCT = DbTypes.CHAR(15)
    BYDGPCTHIST = DbTypes.INT(5)
    GLSUBACCTNO = DbTypes.CHAR(6)
    TRANSLTEATME = DbTypes.CHAR(1)
    GLORIGAPPLCD = DbTypes.INT(1)
    FORMATTEDGL = DbTypes.CHAR(19, 'Formatted GL')
    GLACCTSEG1 = DbTypes.CHAR(10, 'Segment 1')
    GLACCTSEG2 = DbTypes.CHAR(10, 'Segment 2')
    GLACCTSEG3 = DbTypes.CHAR(10, 'Segment 3')
    GLACCTSEG4 = DbTypes.CHAR(10, 'Segment 4')
    GLACCTSEG5 = DbTypes.CHAR(10, 'Segment 5')
    FIXEDASSET = DbTypes.CHAR(10, 'Fixed Asset')
    USERID = DbTypes.CHAR(25)
    UPDPROGRAM = DbTypes.CHAR(25)
    LASTTBLUPD = DbTypes.TIMESTAMP(26)

    def defaults(self):
        return [
            self.COMPANYNO,
            self.DIVISIONNO,
            self.STATUSCODE,
            self.GLACCTNO,
            self.GLTACCTTYPE,
            self.GLTACCTTYPE,
            self.DESCRIPTION,
            self.GLACCTSEG1,
            self.GLACCTSEG2,
            self.GLACCTSEG3,
            self.GLACCTSEG4,
            self.GLACCTSEG5,
            self.FIXEDASSET
        ]


class GLTPST(TableMixin):
    TABLE_NAME = 'GLTPST'

    GLTPSTID = DbTypes.INT(1)
    STATUSCODE = DbTypes.CHAR(20)
    SRCCNCID = DbTypes.INT()
    COMPANYNO = DbTypes.INT()
    DIVISIONNO = DbTypes.INT()
    GLACCTNO = DbTypes.CHAR(16, 'GL Account')
    TRANYR = DbTypes.INT()
    TRANMN = DbTypes.INT()
    TRANDY = DbTypes.INT()
    JOURNALCTL = DbTypes.CHAR(20)
    JOURNALNO = DbTypes.CHAR(20)
    DESCRIPTION = DbTypes.CHAR(25)
    AMOUNT = DbTypes.INT()
    ENTRYPER = DbTypes.INT()
    TRANDATE = DbTypes.CHAR(20)


class GLTROW(TableMixin):
    TABLE_NAME = 'GLTROW'

    GLTROWID = DbTypes.INT(1)
    STATUSCODE = DbTypes.CHAR(20)
    FORMATNO = DbTypes.INT()
    GROUPNO04 = DbTypes.INT()
    DESC40A = DbTypes.CHAR(255)
    SPACEBEFORE = DbTypes.INT()
    SPACEAFTER = DbTypes.INT()
    DBCRCODE = DbTypes.CHAR(5)
    ROACUM = DbTypes.INT()
    ROLNCD = DbTypes.INT()
    RONECP = DbTypes.CHAR(5)
    ROVADC = DbTypes.CHAR(5)


class GLTACT(TableMixin):
    TABLE_NAME = 'GLTACT'

    GLTACTID = DbTypes.INT(1)
    STATUSCODE = DbTypes.CHAR(20)
    COMPANYNO = DbTypes.INT()
    DIVISIONNO = DbTypes.INT()
    GLACCTNO = DbTypes.INT()
    GLTMSTID = DbTypes.INT()
    ACCTYEAR = DbTypes.INT()
    RECTYPECODE = DbTypes.CHAR(5)
    BALFWD = DbTypes.INT()
    PERIOD01 = DbTypes.INT()
    PERIOD02 = DbTypes.INT()
    PERIOD03 = DbTypes.INT()
    PERIOD04 = DbTypes.INT()
    PERIOD05 = DbTypes.INT()
    PERIOD06 = DbTypes.INT()
    PERIOD07 = DbTypes.INT()
    PERIOD08 = DbTypes.INT()
    PERIOD09 = DbTypes.INT()
    PERIOD10 = DbTypes.INT()
    PERIOD11 = DbTypes.INT()
    PERIOD12 = DbTypes.INT()
    PERIOD13 = DbTypes.INT()

class GLTFRN(TableMixin):
    TABLE_NAME = 'GLTFRN'

    GLTFRNID = DbTypes.INT(1)
    STATUSCODE = DbTypes.CHAR(20)
    COMPANYNO = DbTypes.INT()
    DIVISIONNO = DbTypes.INT()
    FORMATNO = DbTypes.INT()
    GROUPNO = DbTypes.INT()
    GLTMSTFMID = DbTypes.INT()
    FROMGLACCT = DbTypes.INT()
    GLTMSTTOID = DbTypes.INT()
    TOGLACCT = DbTypes.INT()
    DBCRCODE = DbTypes.INT()
