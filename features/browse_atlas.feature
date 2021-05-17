
Feature: Browse atlas
    User should be able to visualise and explore a brain atlas.

    Scenario: View Brain Position from Three Planes
        Given I have loaded an atlas
        When I click on a location in the brain
        Then I see a view of that location along the coronal, sagittal, and axial planes.