from nonebot.log import logger
from ..database.models import InfoData
from ..schema import User
from ..api import osu_api

GM = {0: 'osu', 1: 'taiko', 2: 'fruits', 3: 'mania'}
GMN = {'osu': 'Std', 'taiko': 'Taiko', 'fruits': 'Ctb', 'mania': 'Mania'}
FGM = {'osu': 0, 'taiko': 1, 'fruits': 2, 'mania': 3}


async def update_user_info(uid: int):
    for mode in range(4):
        userinfo_dic = await osu_api('update', uid, GM[mode])
        userinfo = User(**userinfo_dic)
        if userinfo.statistics.play_count != 0:
            if info := await InfoData.filter(osu_id=uid, osu_mode=mode).first():
                info.c_rank = userinfo.statistics.country_rank
                info.g_rank = userinfo.statistics.global_rank
                info.pp = userinfo.statistics.pp
                info.acc = round(userinfo.statistics.hit_accuracy, 2)
                info.pc = userinfo.statistics.play_count
                info.count = userinfo.statistics.total_hits
            else:
                info = InfoData(osu_id=uid,
                                c_rank=userinfo.statistics.country_rank,
                                g_rank=userinfo.statistics.global_rank,
                                pp=userinfo.statistics.pp,
                                acc=round(userinfo.statistics.hit_accuracy, 2),
                                pc=userinfo.statistics.play_count,
                                count=userinfo.statistics.total_hits,
                                osu_mode=mode)
        else:
            if info := await InfoData.filter(osu_id=uid, osu_mode=mode).first():
                info.c_rank = userinfo.statistics.country_rank
                info.g_rank = userinfo.statistics.global_rank
                info.pp = userinfo.statistics.pp
                info.acc = round(userinfo.statistics.hit_accuracy, 2)
                info.pc = userinfo.statistics.play_count
                info.count = userinfo.statistics.total_hits
            else:
                info = InfoData(osu_id=uid,
                                c_rank=0,
                                g_rank=0,
                                pp=0,
                                acc=0,
                                pc=0,
                                count=0,
                                osu_mode=mode)
        await info.save()
        logger.info(f'玩家:[{userinfo.username}] {GM[mode]}模式 个人信息更新完毕')

