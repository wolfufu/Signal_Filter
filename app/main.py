from fastapi import FastAPI, HTTPException
import uvicorn

from sim_signal import create_signal, find_freq

app = FastAPI(title="Signal Frequency Detector")

@app.get("/detect_frequencies")
def get_frequency(freq: float):

    if freq < 0.0:
        raise HTTPException(
            status_code=400, 
            detail="Frequency must be greater than or equel 0"
            )
    
    elif freq > 500.0:
        raise HTTPException(
            status_code=400, 
            detail="Frequency must be less than or equal to 500"
            )
    
    t, s, Fs, dt, f_true = create_signal(freq)
    f_detected = find_freq(s, dt)

    return {
        "requested_freq_hz": f_true,
        "detected_frequency_hz": round(f_detected, 3),
        "sampling_rate_hz": Fs,
        "signal_lenght_samples": len(t),
    }
