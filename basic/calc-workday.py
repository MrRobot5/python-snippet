import datetime


if __name__ == "__main__":
    # start = '2021-01-21'
    # today = datetime.datetime.strptime(start, '%Y-%m-%d')
    seq = []
    today = datetime.date.today()
    for x in range(1, 60):
        # 不要使用：today = today.replace(day=today.day - 1)， 这种简单计算，会触发 ValueError: day is out of range for month
        day = today - datetime.timedelta(days=x)
        # exclude Saturday Sunday
        if day.weekday() < 5:
            suffix = day.strftime("%Y-%m-%d")
            seq.append('"{}"'.format(suffix))
    days = " ".join(seq)

    print("arr=({})".format(days))

