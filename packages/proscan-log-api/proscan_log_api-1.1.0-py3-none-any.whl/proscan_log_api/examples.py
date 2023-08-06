"""Slow control example."""
# from time import time

# if __name__ == "__main__":
#     start = time()
#     slow_logs = SlowControlClient(root_dir="/mnt/tcs_logs/")
#     logs = slow_logs.get(
#         system="tvs",
#         folders="g2prod/production/VxWorks/Log/,g3prod/production/VxWorks/Log/,o2prod/production/VxWorks/Log/",
#         start_datetime=datetime(year=2022, month=11, day=30),
#         end_datetime=datetime(year=2022, month=12, day=1),
#         area="G2",
#     )
#     print("execution time: ", time() - start)
#     print(len(logs))

"""TCSTrace Example."""
# if __name__ == "__main__":
#     start = time()
#     trace_logs = TcsTraceClient(root_dir="/mnt/tcs_logs/")
#     logs = trace_logs.get(
#         system="tds",
#         folders="g2prod/production/VxWorks/Log/,g3prod/production/VxWorks/Log/,o2prod/production/VxWorks/Log/",
#         start_datetime=datetime(
#             year=2022,
#             month=12,
#             day=1,
#             hour=10,
#         ),
#         end_datetime=datetime(
#             year=2022,
#             month=12,
#             day=1,
#             hour=11,
#         ),
#         area="G2",
#     )
#     print(len(logs))
#     print("Excecution time: ", time() - start)


"""PASS Example."""
# from time import time

# PASS_LOG_DATA_DIR_ROOT = "/mnt/proscan-fs/"
# PASS_LOG_DATA_FOLDERS = (
#     "PG2TC1-VME-PASS,PG3TC2-VME-PASS,PMPTC1-VME-PASS,PO2TC1-VME-PASS,"
# )
# if __name__ == "__main__":

#     api = PassClient(root_dir=PASS_LOG_DATA_DIR_ROOT, folders=PASS_LOG_DATA_FOLDERS)
#     times = []
#     for i in range(10):
#         start = time()
#         result = api.get(
#             area="G2",
#             # 2023-01-27
#             # timestamp=1674833187487315,
#             end_date=date(year=2022, month=1, day=27),
#             start_date=date(year=2023, month=1, day=27),
#         )
#         result_list = [r for r in result]
#         print(len(result_list))
#         times.append(time() - start)

#     t = 0
#     for _time in times:
#         t = t + _time
#     print("Execution Time average: ", t / 10)
