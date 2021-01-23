
Feature: Section 3D Affine Registration
  # Enter feature description here

  Scenario: Move Section in 3D
    Given I have loaded a section
    When I ask for the section to be translated and rotated
    Then the image is updated with a new 3D transform