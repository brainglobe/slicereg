
Feature: Resample Section
    Users can downsample their slices for performance / visual comparison reasons.

    Scenario: Section Resample
        Given I have a 10um-resolution section loaded
        When I set the resolution to 50um
        Then I should see a 50um resolution slice onscreen