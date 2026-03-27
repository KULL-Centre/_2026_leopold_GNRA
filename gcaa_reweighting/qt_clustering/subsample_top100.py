import numpy as np
import pandas as pd

w_rew = np.load(f"weights/rdcall_CCR_3J_weights_55.6_final.npy")
w_rew_frames = np.column_stack((np.array(range(20100)), w_rew))
df = pd.DataFrame(w_rew_frames)
df.to_csv(f'weights/w_rew_2.dat', index=False)

w_rew_sorted = w_rew_frames[np.argsort(w_rew_frames[:,1])]
np.save(f'weights/w_rew_sorted_weights_frames.npy', w_rew_sorted)
df = pd.DataFrame(w_rew_sorted)
df.to_csv(f'weights/w_rew_sorted_weights_frames.dat', index=False)

frames_rew = np.argsort(w_rew_frames[:,1])
np.save(f'weights/w_rew_sorted_frames.npy', frames_rew)
df = pd.DataFrame(frames_rew)
df.to_csv(f'weights/w_rew_sorted_frames.dat', index=False)

top_frames = []
for frame in range(20000, 20100):
    top_frames.append(frames_rew[frame])
np.save('qt_clustering_top/w_rew_top_100_frames.npy', top_frames)
pd.DataFrame(top_frames).to_csv('qt_clustering_top/w_rew_top_100_frames.dat', index=False)