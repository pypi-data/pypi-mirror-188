
from sparrow_order_lib.sparrow_disstorage.models import StorageRecord

from sparrow_afsplus.models import DistributeAfsplus
from sparrow_disstorage.serializers import StorageRecordOnlyShelfInfoSerializer

def get_seats_by_dis_ids(dis_ids):
    """ 由发货单 id 获取货位信息 """
    dis_ids_nonredundant = list(set(dis_ids))

    storage_records = StorageRecord.objects.filter(
        distribute_id__in=dis_ids_nonredundant, if_out=False).all()
    storage_records_data = StorageRecordOnlyShelfInfoSerializer(storage_records, many=True).data

    return {sr['distribute_id']: sr for sr in storage_records_data}

