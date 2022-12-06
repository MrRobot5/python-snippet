import datetime


if __name__ == "__main__":
    # start = '2021-01-21'
    # today = datetime.datetime.strptime(start, '%Y-%m-%d')
    seq = []
    today = datetime.date.today()
    for x in range(1, 15):
        day = today - datetime.timedelta(days=x)
        # exclude Saturday Sunday
        if day.weekday() < 5:
            suffix = day.strftime("%Y-%m-%d")
            seq.append('"{}"'.format(suffix))
    days = " ".join(seq)

    print("arr=({})".format(days))

