Swarm-Sim

Swarm-Sim is a powerful and interactive 2D and 3D simulation platform designed for research, education, and development of swarm robotics and agent-based systems. It allows users to visualize, configure, and control multiple agents in real-time within a customizable environment.

Swarm-Sim supports experimentation with behavior algorithms, scaling effects, and visual analytics to understand emergent behaviors of decentralized systems. Whether you’re a student, researcher, or enthusiast in AI, robotics, or distributed systems—Swarm-Sim brings your swarm intelligence ideas to life.

⸻

🚀 Features
    •    Real-time 2D/3D visualization of swarm behavior
    •    Agent, item, and location scaling with dynamic sliders
    •    Scenario saving and replay features
    •    Screenshots and vector export for publication
    •    Control over grid, camera, lighting, and projection
    •    Platform-agnostic: works on Linux, Windows, macOS (including M1/M2 Apple Silicon)

⸻

🛠 Installation

Step-by-Step (Linux, macOS, Windows):
    1.    Clone the repository:

   git clone https://github.com/YOUR_USERNAME/swarmsim.git
   cd swarmsim

    2.    Create and activate a virtual environment:

   python3 -m venv venv
   source venv/bin/activate       # macOS/Linux
   .\venv\Scripts\activate       # Windows

    3.    Install dependencies:

   pip install -r requirements.txt



⸻

▶️ Running Swarm-Sim

After installation, run the simulator with:

python3 swarm-sim.py

If you’re using PyCharm or another IDE, make sure to select the correct virtual environment as your interpreter.

⸻

📦 Requirements

The following Python libraries are required and listed in requirements.txt:
    •    numpy
    •    pandas
    •    PyOpenGL
    •    Pillow
    •    PyQt5
    •    opencv-python

These will be installed automatically with:

pip install -r requirements.txt



⸻

📌 Notes

For legacy systems (e.g., Ubuntu 14.04), you may need:

pip install PyQt5==5.10.1

For OpenGL rendering issues, ensure your system supports OpenGL >= 2.0 and your windowing system is properly initialized.

⸻

📜 License

MIT License

⸻

👩‍💻 Contributors
    •    Original Author: Dr. Ahmad Reza Cheraghi
    •    Contributions Welcome!
