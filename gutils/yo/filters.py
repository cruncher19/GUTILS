#!/usr/bin/env python

import numpy as np

from gutils.yo import (
    TIME_DIM,
    DATA_DIM
)


def default_filter(dataset):
    dataset = filter_profile_depth(dataset)
    dataset = filter_profile_number_of_points(dataset)
    dataset = filter_profile_time(dataset)
    dataset = filter_profile_distance(dataset)

    return dataset


def filter_profiles(dataset, conditional):
    """Filters out profiles that do not meet some criteria

    Returns the filtered set of profiles
    """

    filtered_dataset = dataset.copy()

    filtered_dataset[:, 2] = 0

    start_index = 0
    last_good_profile = 0
    num_profiles = int(max(dataset[:, 2]) + 1)
    for profile_id in range(0, num_profiles):
        profile = dataset[dataset[:, 2] == profile_id]
        end_index = np.where(dataset[:, 2] == profile_id)[0][-1] + 1
        if conditional(profile):
            filtered_dataset[start_index:end_index, 2] = last_good_profile
            start_index = end_index
            last_good_profile += 1
        elif len(dataset) == end_index:
            filtered_dataset[start_index:, 2] = last_good_profile

    return filtered_dataset

# Convenience methods follow


def filter_profile_depth(dataset, below=None):
    """Filters out profiles that are not below a certain depth (Default: 1m)

    Returns the filtered set of profiles
    """
    below = below or 1

    def conditional(profile):
        depth_max = max(profile[:, DATA_DIM])
        return depth_max >= below

    return filter_profiles(dataset, conditional)


def filter_profile_time(dataset, timespan_condition=None):
    """Filters out profiles that do not span a specified number of seconds
    (Default: 10 seconds)

    Returns the filtered set of profiles
    """
    timespan_condition = timespan_condition or 10

    def conditional(profile):
        timespan = profile[-1, TIME_DIM] - profile[0, TIME_DIM]
        return timespan >= timespan_condition

    return filter_profiles(dataset, conditional)


def filter_profile_distance(dataset, distance_condition=None):
    """Filters out profiles that do not span a specified vertical distance
    (Default: 1m)

    Returns the filtered set of profiles
    """
    distance_condition = distance_condition or 1

    def conditional(profile):
        distance = abs(profile[-1, DATA_DIM] - profile[0, DATA_DIM])
        return distance >= distance_condition

    return filter_profiles(dataset, conditional)


def filter_profile_number_of_points(dataset, points_condition=None):
    """Filters out profiles that do not have a specified number of points
    (Default: 5 points)

    Returns the filtered set of profiles
    """
    points_condition = points_condition or 5

    def conditional(profile):
        return len(profile) >= points_condition

    return filter_profiles(dataset, conditional)
