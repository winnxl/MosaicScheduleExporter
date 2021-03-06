# Placeholder
import connector
import converter

# Test Inputs
parser_out = [#('ECON 1BB3 - Introductory Macroeconomics', 'Lecture', 'We 2:30PM - 3:20PM', 'MDCL 1305', '2019/01/07 - 2019/04/09'),
 #('ECON 1BB3 - Introductory Macroeconomics', 'Tutorial', 'Fr 12:30PM - 1:20PM', 'ABB 271', '2019/01/07 - 2019/04/09'),
 ('SFWRENG 2FA3 - Discrete Math. Application II', 'Lecture', 'TuThFr 11:30AM - 12:20PM', 'ITB 137', '2019/01/07 - 2019/04/09'),
 # ('SFWRENG 2FA3 - Discrete Math. Application II', 'Tutorial', 'Mo 11:30AM - 12:20PM', 'BSB 108', '2019/01/07 - 2019/04/09'),
 # ('SFWRENG 3A04 - Software Design III', 'Lecture', 'TuWeFr 3:30PM - 4:20PM', 'HH 109', '2019/01/07 - 2019/04/09'),
 # ('SFWRENG 3A04 - Software Design III', 'Tutorial', 'Mo 3:30PM - 5:20PM', 'ABB 164', '2019/01/07 - 2019/04/09'),
 # ('SFWRENG 3S03 - Software Testing', 'Lecture', 'MoWeTh 1:30PM - 2:20PM', 'CNH B107', '2019/01/07 - 2019/04/09'),
 # ('SFWRENG 3S03 - Software Testing', 'Tutorial', 'Tu 4:30PM - 5:20PM', 'ETB 235', '2019/01/07 - 2019/04/09'),
 # ('SFWRENG 4C03 - Comp Networks & Security', 'Lecture', 'MoWeTh 5:30PM - 6:20PM', 'JHE 264', '2019/01/07 - 2019/04/09'),
 # ('SFWRENG 4C03 - Comp Networks & Security', 'Laboratory', 'Fr 8:30AM - 11:20AM', 'ITB 236', '2019/01/07 - 2019/01/12'),
 # ('SFWRENG 4C03 - Comp Networks & Security', 'Laboratory', 'Fr 8:30AM - 11:20AM', 'ITB 236', '2019/01/21 - 2019/01/26'),
 # ('SFWRENG 4C03 - Comp Networks & Security', 'Laboratory', 'Fr 8:30AM - 11:20AM', 'ITB 236', '2019/02/04 - 2019/02/09'),
 # ('SFWRENG 4C03 - Comp Networks & Security', 'Laboratory', 'Fr 8:30AM - 11:20AM', 'ITB 236', '2019/02/18 - 2019/02/23'),
 ('SFWRENG 4C03 - Comp Networks & Security', 'Laboratory', 'Fr 8:30AM - 11:20AM', 'ITB 236', '2019/03/04 - 2019/03/09'),
 ('SFWRENG 4C03 - Comp Networks & Security', 'Laboratory', 'Fr 8:30AM - 11:20AM', 'ITB 236', '2019/03/18 - 2019/03/23'),
 ('SFWRENG 4C03 - Comp Networks & Security', 'Laboratory', 'Fr 8:30AM - 11:20AM', 'ITB 236', '2019/04/01 - 2019/04/06')]

c = connector.Connector(converter.Converter.convert(parser_out))
c.login()
input("press key to push test schedule...")
c.push_to_schedule()
input("press key to remove and logout...")
c.remove_new_cal()
# c.logout()
