# Created by Nick at 13/01/2021
Feature: Multichannel Image Data
  Import and Visualize multichannel sections

  Scenario: Switch Channels
    Given I have loaded an image with 2 channels
    And I am viewing channel 1
    When I ask for channel 2
    Then the onscreen section data changes to channel 2