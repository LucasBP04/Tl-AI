import os
import traci
import numpy as np

class SumoEnvDQN_J5:
    def __init__(self, sumo_cfg_path, use_gui=False, delta_time=5):
        # sumo_cfg_path: pásalo ABSOLUTO desde train_dqn_sumo.py
        self.sumo_cfg = sumo_cfg_path
        self.use_gui = use_gui
        self.delta_time = delta_time
        self.tl_id = "J5"

        # Carriles EXACTOS de tu red
        self.lanes_norte = ["-E4_0", "-E4_1", "-E4_2"]
        self.lanes_este  = ["E5_0", "E5_1", "E5_2"]
        self.lanes_sur   = ["E6.0_0", "E6.0_1", "E6.0_2"]
        self.lanes_oeste = ["E3_0", "E3_1", "E3_2"]
        self.all_lanes = (
            self.lanes_norte +
            self.lanes_este +
            self.lanes_sur +
            self.lanes_oeste
        )

        # 0 = mantener fase, 1 = ir a la siguiente
        self.n_actions = 2
        self.n_phases = None  # la llenamos en reset()

    def _start_sumo(self):
        sumo_binary = "sumo-gui" if self.use_gui else "sumo"
        print("Lanzando SUMO con config:", self.sumo_cfg)
        traci.start([sumo_binary, "-c", self.sumo_cfg, "--no-step-log", "true"])

    def reset(self):
        if traci.isLoaded():
            traci.close()
        self._start_sumo()
        self.current_step = 0

        # Usar el programa 0 (el lógico que definiste en Mi_red.net.xml)
        traci.trafficlight.setProgram(self.tl_id, "0")
        traci.trafficlight.setPhase(self.tl_id, 0)

        # Obtener número de fases del semáforo J5
        logic_list = traci.trafficlight.getCompleteRedYellowGreenDefinition(self.tl_id)
        logic = logic_list[0]              # normalmente solo hay un programa
        self.n_phases = len(logic.phases)
        print("Semáforo", self.tl_id, "tiene", self.n_phases, "fases")

        return self._get_state()

    def _get_state(self):
        veh_norte = sum(traci.lane.getLastStepVehicleNumber(l) for l in self.lanes_norte)
        veh_este  = sum(traci.lane.getLastStepVehicleNumber(l) for l in self.lanes_este)
        veh_sur   = sum(traci.lane.getLastStepVehicleNumber(l) for l in self.lanes_sur)
        veh_oeste = sum(traci.lane.getLastStepVehicleNumber(l) for l in self.lanes_oeste)

        phase = traci.trafficlight.getPhase(self.tl_id)  # índice de fase actual

        state = np.array([veh_norte, veh_este, veh_sur, veh_oeste, phase], dtype=np.float32)
        return state

    def _get_reward(self):
        # Recompensa = negativo del tiempo de espera total en todos los carriles de entrada
        wait_time = sum(traci.lane.getWaitingTime(l) for l in self.all_lanes)
        return -wait_time

    def step(self, action):
        current_phase = traci.trafficlight.getPhase(self.tl_id)

        # Usamos self.n_phases que calculamos en reset()
        n_phases = self.n_phases

        # acción 1 => ir a la siguiente fase (0->1->2->...->n-1->0)
        if action == 1:
            next_phase = (current_phase + 1) % n_phases
            traci.trafficlight.setPhase(self.tl_id, next_phase)
        # acción 0 => mantener fase actual

        # Avanzar SUMO delta_time segundos
        for _ in range(self.delta_time):
            traci.simulationStep()
            self.current_step += 1

        state = self._get_state()
        reward = self._get_reward()
        done = traci.simulation.getMinExpectedNumber() <= 0

        return state, reward, done, {}
import os
import traci
import numpy as np

class SumoEnvDQN_J5:
    def __init__(self, sumo_cfg_path, use_gui=False, delta_time=5):
        # sumo_cfg_path: pásalo ABSOLUTO desde train_dqn_sumo.py
        self.sumo_cfg = sumo_cfg_path
        self.use_gui = use_gui
        self.delta_time = delta_time
        self.tl_id = "J5"

        # Carriles EXACTOS de tu red
        self.lanes_norte = ["-E4_0", "-E4_1", "-E4_2"]
        self.lanes_este  = ["E5_0", "E5_1", "E5_2"]
        self.lanes_sur   = ["E6.0_0", "E6.0_1", "E6.0_2"]
        self.lanes_oeste = ["E3_0", "E3_1", "E3_2"]
        self.all_lanes = (
            self.lanes_norte +
            self.lanes_este +
            self.lanes_sur +
            self.lanes_oeste
        )

        # 0 = mantener fase, 1 = ir a la siguiente
        self.n_actions = 2
        self.n_phases = None  # la llenamos en reset()

    def _start_sumo(self):
        sumo_binary = "sumo-gui" if self.use_gui else "sumo"
        print("Lanzando SUMO con config:", self.sumo_cfg)
        traci.start([sumo_binary, "-c", self.sumo_cfg, "--no-step-log", "true"])

    def reset(self):
        if traci.isLoaded():
            traci.close()
        self._start_sumo()
        self.current_step = 0

        # Usar el programa 0 (el lógico que definiste en Mi_red.net.xml)
        traci.trafficlight.setProgram(self.tl_id, "0")
        traci.trafficlight.setPhase(self.tl_id, 0)

        # Obtener número de fases del semáforo J5
        logic_list = traci.trafficlight.getCompleteRedYellowGreenDefinition(self.tl_id)
        logic = logic_list[0]              # normalmente solo hay un programa
        self.n_phases = len(logic.phases)
        print("Semáforo", self.tl_id, "tiene", self.n_phases, "fases")

        return self._get_state()

    def _get_state(self):
        veh_norte = sum(traci.lane.getLastStepVehicleNumber(l) for l in self.lanes_norte)
        veh_este  = sum(traci.lane.getLastStepVehicleNumber(l) for l in self.lanes_este)
        veh_sur   = sum(traci.lane.getLastStepVehicleNumber(l) for l in self.lanes_sur)
        veh_oeste = sum(traci.lane.getLastStepVehicleNumber(l) for l in self.lanes_oeste)

        phase = traci.trafficlight.getPhase(self.tl_id)  # índice de fase actual

        state = np.array([veh_norte, veh_este, veh_sur, veh_oeste, phase], dtype=np.float32)
        return state

    def _get_reward(self):
        # Recompensa = negativo del tiempo de espera total en todos los carriles de entrada
        wait_time = sum(traci.lane.getWaitingTime(l) for l in self.all_lanes)
        return -wait_time

    def step(self, action):
        current_phase = traci.trafficlight.getPhase(self.tl_id)

        # Usamos self.n_phases que calculamos en reset()
        n_phases = self.n_phases

        # acción 1 => ir a la siguiente fase (0->1->2->...->n-1->0)
        if action == 1:
            next_phase = (current_phase + 1) % n_phases
            traci.trafficlight.setPhase(self.tl_id, next_phase)
        # acción 0 => mantener fase actual

        # Avanzar SUMO delta_time segundos
        for _ in range(self.delta_time):
            traci.simulationStep()
            self.current_step += 1

        state = self._get_state()
        reward = self._get_reward()
        done = traci.simulation.getMinExpectedNumber() <= 0

        return state, reward, done, {}
