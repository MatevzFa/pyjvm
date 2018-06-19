class Executor:

    def __init__(self, vm, java_class, main_method, m_args):
        """

        :type vm: pyjvm.vm.VM
        :param vm:
        :param java_class:
        :param main_method:
        :param m_args:
        """

        self.vm = vm
        self.java_class = java_class
        self.main_method = main_method
        self.m_args = m_args

        vm.initialize_vm(java_class, main_method, m_args)

        # self.current_thread = vm.get_next_thread()

    def get_frame_for_thread(self, thread_idx):
        """

        :param thread_idx: index of the thread
        :return: Current frame of the specified thread
        :rtype: pyjvm.frame.Frame
        """
        if len(self.vm.threads[thread_idx].frame_stack) > 0:
            return self.vm.threads[thread_idx].frame_stack[-1]
        else:
            return None

    def run_all(self):
        """
        Executes all threads
        :return: None
        """
        while True:
            if not self.step_all_threads(quota=1000):
                break

    def step_thread(self, thread_idx, quota=1):
        """
        Run a single bytecode from thread with index thread_idx
        :param thread_idx: index of the thread to exec
        :return: true if the thread is still alive after exec, false otherwise
        """
        thread = self.vm.threads[thread_idx]
        if thread.is_alive:
            frame = self.get_frame_for_thread(thread_idx)
            op = frame.get_current_bytecode()
            operands = frame.get_current_operands()
            self.vm.run_thread(thread, quota)
            print "{0} | {1} {2}".format(thread_idx, op, str(operands))
            if len(thread.frame_stack) == 0:
                self.kill_thread(thread)
                return False
            else:
                return True
        else:
            return False

    def step_all_threads(self, quota=1):
        """
        Run quota bytecodes for every thread
        :param quota: n of bytecodes (default 1)
        :return: true if any thread is still alive after exec, false otherwise
        """
        any_alive = False
        for thread_idx in range(len(self.vm.threads)):
            thread = self.vm.threads[thread_idx]
            if thread.is_alive:
                self.step_thread(thread_idx, quota)
                if len(thread.frame_stack) == 0:
                    self.kill_thread(thread)
                else:
                    any_alive = True
        return any_alive and self.vm.non_daemons > 0

    def kill_thread(self, thread):
        """
        Kill the specified thread
        :param thread: the thread
        :return: None
        """
        thread.is_alive = False
        j_thread = self.vm.heap[thread.java_thread[1]]
        assert j_thread is not None
        for o in j_thread.waiting_list:
            o.is_notified = True
        java_thread = self.vm.heap[thread.java_thread[1]]
        if java_thread.fields["daemon"] == 0:
            self.vm.non_daemons -= 1
            if self.vm.non_daemons == 0:
                pass
