
Feature: Browse atlas
    User should be able to visualise and explore a brain atlas.

    Scenario: View Brain Position from Three Planes
        Given the 25um atlas is currently loaded
        And that the current position is at the origin
        When I click on a location in the coronal section
        Then I see a view of that location along the sagittal plane.
        And I see a view of that location along the axial plane.