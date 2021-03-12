import models
import graphics as graph


def task1_solve(Tc, Ts):
    channels = 1
    model = models.ModelWithoutQueue(client_t=Tc, handling_t=Ts, channels=channels)
    plots = graph.ModelPlots(name="Model without queue")

    denials = [model.denial_prob()]
    channels_busy = [model.busy_operators()]
    busy_coefs = [model.busy_coefficient()]

    while denials[channels - 1] >= 0.01:
        channels += 1
        model.channels = channels
        denials.append(model.denial_prob())
        channels_busy.append(model.busy_operators())
        busy_coefs.append(model.busy_coefficient())

    plots.show_feature_dep_chan(channels=channels, data=denials, label="Probability of denial")
    plots.show_feature_dep_chan(channels=channels, data=channels_busy, label="Math expect of busy operators")
    plots.show_feature_dep_chan(channels=channels, data=busy_coefs, label="Busy channels coefficient")

    return channels
