import os
import wfdb


def get_all_signal_ids() -> list[int]:
    """gets all valid signal ids from mit bih arrythmia database

    Returns:
        list[int]: signal ids
    """
    dir = "mit-bih-arrhythmia-database-1.0.0"
    signal_ids = [int(file.split(".")[0])
                  for file in os.listdir(dir) if file.endswith(".dat")]
    return signal_ids


def get_record(signal_id: int, start: int = 0, end: int = None) -> list[float]:
    """ return wfdb record

    Args:
        signal_id (int): id of the signal
        start (int, optional): start value. Defaults to 0.
        end (int, optional): end value. Defaults to None.

    Returns:
        Record
    """
    signal_path = os.path.join(
        'mit-bih-arrhythmia-database-1.0.0', str(signal_id))
    record = wfdb.rdrecord(signal_path, sampfrom=start, sampto=end)
    return record


def get_signal(signal_id: int, start: int = 0, end: int = None):
    """ gets p signal of a singular signal with a given range

    Args:
        signal_id (int): id of the signal
        start (int, optional): start value. Defaults to 0.
        end (int, optional): end value. Defaults to None.

    Returns:
        list[float]: signal for the signal
    """
    record = get_record(signal_id, start, end)
    channel_0 = [signal[0] for signal in record.p_signal]
    return channel_0


def get_annotations(signal_id: int, start: int = 0, end: int = None):
    """ gets annotation of a singular signal with a given range

    Args:
        signal_id (int): id of the signal
        start (int, optional): start value. Defaults to 0.
        end (int, optional): end value. Defaults to None.

    Returns:
        Annotation
    """
    signal_path = os.path.join(
        'mit-bih-arrhythmia-database-1.0.0',
        str(signal_id)
    )
    ann = wfdb.rdann(signal_path, sampfrom=start, sampto=end, extension="atr")
    return ann


def get_all_signals(start: int = 0, end: int = None) -> list[list[float]]:
    signal_ids = get_all_signal_ids()
    signals = [get_signal(signal_id=signal_id, start=start, end=end)
               for signal_id in signal_ids]
    return signals


def get_all_annotations(start: int = 0, end: int = None):
    signal_ids = get_all_signal_ids()
    signals = [get_annotations(
        signal_id=signal_id, start=start, end=end) for signal_id in signal_ids]
    return signals
