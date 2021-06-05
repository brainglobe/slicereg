
Feature: Section 3D Affine Registration
  # Enter feature description here

  Examples:
  | operation_type | axis | amount |
  | translate      | longitudinal    | 10     |
  | translate      | anteroposterior    | 8      |
  | translate      | horizontal    | 26.2   |
  | rotate         | longitudinal    | -45.2  |
  | rotate         | anteroposterior    | 239.34 |
  | rotate         | horizontal    | 0.01   |

  Scenario Outline: Move Section in 3D
    Given I have loaded a section
    When I <operation_type> the section along the <axis> axis by <amount>
    Then the image is updated with a new 3D transform
    And an atlas section image at that transform is shown.

  Scenario Outline: Set Section's 3D Coordinates
    Given I have loaded a section
    When I <operation_type> the section along the <axis> axis by <amount>
    Then the image is updated with a new 3D transform with indicated paramters set to the requested value
    And an atlas section image at that transform is shown.

  Scenario: Check Pixel Coordinate in Atlas Space
    Given I have loaded a section
    When I indicate a section image coordinate
    Then the coordinate's 2D position and 3D position should appear

