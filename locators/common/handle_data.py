# encoding: utf-8
# @File  : handle_data.py
# @Author: Fan Jing
# @Date  : 2026/08/21/15:47
from faker import Faker
from loguru import logger
import random
from datetime import datetime, timedelta


def get_random_username():
    """
    随机生成用户名
    :return:
    """
    faker = Faker(locale='zh_CN')
    while True:
        username = faker.user_name()
        if username[0].isalpha() and 4 <= len(username) <= 10:
            logger.info(f"随机生成的用户名是：{username}")
            break
    return username


def get_random_email(domain=None):
    """
    随机生成邮箱，支持多种邮箱格式
    :param domain: 指定邮箱域名，如 'qq.com', 'gmail.com' 等，None则随机选择
    :return: 邮箱地址
    """
    faker = Faker(locale='en_US')

    common_domains = [
        'qq.com', '163.com', '126.com', 'gmail.com',
        'outlook.com', 'hotmail.com', 'yahoo.com',
        'sina.com', 'sohu.com', 'foxmail.com'
    ]

    username = faker.user_name()
    selected_domain = domain if domain else random.choice(common_domains)
    email = f"{username}@{selected_domain}"

    logger.info(f"随机生成的邮箱是：{email}")
    return email


def get_random_phone(country='MY', with_country_code=False):
    """
    随机生成手机号，支持多国格式
    :param country: 国家代码，'MY'=马来西亚, 'CN'=中国, 默认马来西亚
    :param with_country_code: 是否包含国际区号，默认False（注册用），True用于登录
    :return: 手机号字符串
    """
    faker = Faker(locale='zh_CN')

    if country == 'MY':
        mobile_prefixes = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
        prefix = random.choice(mobile_prefixes)
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        phone_number = f"{prefix}{suffix}"

        if with_country_code:
            full_phone = f"60{phone_number}"
            logger.info(f"随机生成的马来西亚手机号（含区号）：{full_phone}")
            return full_phone
        else:
            logger.info(f"随机生成的马来西亚手机号：{phone_number}")
            return phone_number

    elif country == 'CN':
        while True:
            phone = faker.phone_number()
            if phone.startswith('1') and len(phone) == 11:
                if with_country_code:
                    full_phone = f"86{phone}"
                    logger.info(f"随机生成的中国手机号（含区号）：{full_phone}")
                    return full_phone
                else:
                    logger.info(f"随机生成的中国手机号：{phone}")
                    return phone
    else:
        phone = faker.phone_number()
        logger.info(f"随机生成的手机号：{phone}")
        return phone


def get_random_date(days_range=7, date_format="%Y-%m-%d"):
    """
    随机生成一个日期，默认生成今天之后 0~7 天内的随机日期
    :param days_range: 日期范围（天数），默认 7 天
    :param date_format: 日期格式，默认 YYYY-MM-DD
    :return: 日期字符串，如 '2026-08-25'
    """
    today = datetime.now()
    random_days = random.randint(0, days_range)
    random_date = today + timedelta(days=random_days)
    date_str = random_date.strftime(date_format)
    logger.info(f"随机生成的日期：{date_str}")
    return date_str


def get_random_date_range(days_range=7, date_format="%Y-%m-%d"):
    """
    随机生成一对起止日期（开始日期 <= 结束日期）
    :param days_range: 日期范围（天数），默认 7 天
    :param date_format: 日期格式
    :return: (start_date, end_date) 元组
    """
    start = get_random_date(days_range, date_format)
    # 结束日期 >= 开始日期
    start_dt = datetime.strptime(start, date_format)
    end_days = random.randint(0, days_range)
    end_dt = start_dt + timedelta(days=end_days)
    end = end_dt.strftime(date_format)
    logger.info(f"随机生成的日期范围：{start} ~ {end}")
    return start, end
