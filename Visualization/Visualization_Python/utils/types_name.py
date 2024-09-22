DIE = 'die'
QUAD = 'quad'
CBU = 'Cbu'
TCU = 'Tcu'
ECORE = 'Ecore'
HBM = 'hbm'
BMT = 'bmt'
CBUS_INJ = 'cbus inj'
CBUS_CLT = 'cbus clt'
NFI_INJ = 'nfi inj'
NFI_CLT = 'nfi clt'
H2G = 'H2G'
G2H = 'G2H'
PCIE = 'pcie'
MCU = 'MCU'
IQR = 'iqr'
IQD = 'iqd'
LNB = 'lnb'
HOST_INTERFACE = 'Host_interface'
D2D = 'd2d'
EQ = 'eq'
IRQA = 'irqa'
BIN = 'bin'


AREAS = {
    'hbm': HBM,
    'd2d': D2D,
    'bmt': BMT,
    'host if': HOST_INTERFACE,
    'pcie': PCIE,
    'ecore req cip': ECORE,
    'ecore rsp cip': ECORE,
    'mcu gate 1': MCU,
    'mcu gate 0': MCU,
    'mem0': CBU,
    'mem1': CBU,
    'lcip': CBU,
    'nfi': LNB
}
UNIT_MAP = {
    'bmt': BMT,
    'pcie': PCIE,
    'cbus inj': CBUS_INJ,
    'cbus clt': CBUS_CLT,
    'nfi inj': NFI_INJ,
    'nfi clt': NFI_CLT,
    'eq': EQ,
    'hbm': HBM,
    'tcu': TCU,
    'iqr': IQR,
    'iqd': IQD,
    'bin': BIN,
    'lnb': LNB
}

