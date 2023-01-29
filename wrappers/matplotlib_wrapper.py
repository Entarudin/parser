from time import time
from hashlib import md5
import matplotlib.pyplot as plt
from models import StatisticsThreats
from constants import TypeThreatsEnum


class MatplotlibWrapper:
    def get_statisctics_chart(self, statistics: StatisticsThreats) -> tuple:
        img_id = md5(str('statistisc' + str(time())).encode()).hexdigest()
        filename = f'images/{img_id}.png'

        labels = [
            TypeThreatsEnum.THREAT_TYPE.value,
            TypeThreatsEnum.VULNERABILITY_TYPE.value,
            TypeThreatsEnum.INCIDENT_TYPE.value,
            TypeThreatsEnum.ATTACK_TYPE.value
        ]
        values = [
            statistics.count_threats,
            statistics.count_vulnerabilities,
            statistics.count_incidents,
            statistics.count_attacks
        ]

        fig1, ax1 = plt.subplots()
        res = ax1.pie(
            values, labels=labels, autopct='%1.1f%%',
            wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"},  rotatelabels=True
        )
        plt.savefig(filename)
        return img_id, res
