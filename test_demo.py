# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
import threading

m_li = [3, 4, 5, 6]


class TestThread:
    @pytest.mark.thread
    @pytest.mark.parametrize('case', m_li)
    def test_thread(self, case):
        print(case**2)

    def func(self):
        threads = []

        for i in m_li:
            t = threading.Thread(target=self.test_thread, args=(i,))
            threads.append(t)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == '__main__':
    TestThread().func()
