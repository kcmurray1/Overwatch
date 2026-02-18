# Tailscale Manager
Installs and adds machines to a tailnet created with the tailscale admin dashboard.

## Implementation
Uses a Tailscale OAuth key to generate temporary access tokens to onboard machines into a tailnet associated with a tag name.

## OS handling
This manager expects an BaseOS type object that has the install_tailscale() method implemented. 
- **Linux** is the only fully support OS. The Tailscale Manager can install and add the machine into an existing tailnet
- **Windows** requires manual installation of the tailscale client. Adding the machine to an existing tailent is the only support Tailscale Manager offers.