from pyrogram import Client
from pagermaid.listener import listener
from pagermaid.utils import Message,pip_install
from datetime import datetime, timedelta

pip_install("oci")
import oci
# 配置文件路径
path_to_config = r'./plugins/configs/seoul.conf'
# 配置文件[]内的"标题"
config_title = 'Seoul'
# 命令名
command_name = 'obdt'

def get_this_month():
    current_time = datetime.now()
    month_start = current_time.replace(day=1)
    if current_time.month == 12:
        next_month = month_start.replace(year=current_time.year + 1, month=1)
    else:
        next_month = month_start.replace(month=current_time.month + 1)
    month_end = next_month - timedelta(days=1)
    formatted_month_start = month_start.strftime("%Y-%m-%dT00:00:00Z")
    formatted_month_end = month_end.strftime("%Y-%m-%dT00:00:00Z")
    return formatted_month_start, formatted_month_end


def get_previous_month():
    current_time = datetime.now()
    current_time = current_time.replace(day=1)
    month_end = current_time - timedelta(days=1)
    month_start = month_end.replace(day=1)
    formatted_month_start = month_start.strftime("%Y-%m-%dT00:00:00Z")
    formatted_month_end = month_end.strftime("%Y-%m-%dT00:00:00Z")
    return formatted_month_start, formatted_month_end


async def get_outbound(date_you_choose: str = 'current'):
    config = oci.config.from_file(path_to_config, config_title)
    tenant_id = config['tenancy']
    usage_client = oci.usage_api.UsageapiClient(config)
    if date_you_choose in ['last', 'l', 'previous', 'p']:
        time_usage_started, time_usage_ended = get_previous_month()
    elif date_you_choose in ['this', 'current', 't', 'c', '']:
        time_usage_started, time_usage_ended = get_this_month()
    else:
        return "错误的时间类型"
    try:
        outbound_monthly_usage_model = oci.usage_api.models.RequestSummarizedUsagesDetails(
            tenant_id=tenant_id,
            granularity='MONTHLY',
            query_type='USAGE',
            group_by=['resourceId', 'skuName'],
            time_usage_started=time_usage_started,
            time_usage_ended=time_usage_ended,
            compartment_depth=2
        )
        outbound_monthly_usage_ = usage_client.request_summarized_usages(
            outbound_monthly_usage_model
        )
        instance_usage, bucket_usage = 0, 0
        instance_usage_text, bucket_usage_text = '', ''
        for item in outbound_monthly_usage_.data.items:
            if 'ocid1.vnic.' in item.resource_id:
                network_client = oci.core.VirtualNetworkClient(config)
                vnic_ocid = str(item.resource_id)
                try:
                    response = network_client.get_vnic(vnic_ocid)
                    vnic_name = response.data.display_name
                except oci.exceptions.ServiceError as e:
                    vnic_name = '已删除的网卡'
                instance_usage_text += (f'`{vnic_name}` | `{item.computed_quantity:.3f}GB`\n')
                instance_usage += item.computed_quantity
            if 'Object Storage - Outbound Data Transfer' in item.sku_name:
                bucket_usage += item.computed_quantity
        total = instance_usage + bucket_usage
        result = (
            f'甲骨文云出站流量\n'
            f'开始时间: `{time_usage_started}`\n'
            f'结束时间: `{time_usage_ended}`\n'
            f'网卡名称 | 出站流量\n'
            f'\n'
            f'{instance_usage_text}'
            f'\n'
            f'实例出站流量: `{instance_usage:.3f}GB`\n'
            f'存储桶出站流量: `{bucket_usage:.3f}GB`\n'
            f'总出站流量: `{total:.3f}GB`'
        )
        return result
    except oci.exceptions.ServiceError as e:
        return "Service Error"
    except Exception as e:
        return "Exception Error"


@listener(
    command=command_name,
    parameters="[last/l/previous/p]",
    description="无参数默认获取本月, 带正确参数为获取上月出站流量"
)
async def oracle_cloud_infrastructure_outbound_data_transfer(message: Message):
    params = message.parameter
    if len(params) < 1:
        await message.edit(f'获取本月出站流量中')
        context = await get_outbound()
        await message.edit(context)
        return
    elif len(params) < 2:
        await message.edit(f'获取上月出站流量中')
        context = await get_outbound(params[0])
        await message.edit(context)
        return
