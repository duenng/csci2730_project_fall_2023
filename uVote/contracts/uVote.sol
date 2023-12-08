// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract uVote is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    struct Vote {
        mapping(uint256 => uint256) optionCounts; // Counts votes for each option
    }

    struct Ballot {
        mapping(address => bool) hasVoted; // Tracks if an address has voted
        Vote count; // Vote counts for this ballot
        bool votingOpen; // Indicates if the voting is open
        uint256[] options; // Array of option IDs
        uint256 maxChoices; // Maximum number of choices allowed per vote
    }

    mapping(uint256 => Ballot) private ballots;
    uint256 public nextBallotId;

    event VoteStarted(uint256 ballotId);
    event Voted(address indexed voter, uint256 ballotId, uint256[] selectedOptions);
    event VoteEnded(uint256 ballotId, uint256[] optionCounts);

    constructor() {
        _setupRole(ADMIN_ROLE, msg.sender);
    }

    function isVotingOpen(uint256 ballotId) public view returns (bool) {
        return ballots[ballotId].votingOpen;
    }

    function getMaxChoices(uint256 ballotId) public view returns (uint256) {
        return ballots[ballotId].maxChoices;
    }

    function getOptionCount(uint256 ballotId, uint256 option) public view returns (uint256) {
        return ballots[ballotId].count.optionCounts[option];
    }

    function hasVoted(uint256 ballotId, address voter) public view returns (bool) {
        return ballots[ballotId].hasVoted[voter];
    }

    function startVote(uint256[] memory _options, uint256 _maxChoices) public onlyRole(ADMIN_ROLE) {
        uint256 ballotId = nextBallotId++;
        ballots[ballotId].votingOpen = true;
        ballots[ballotId].options = _options;
        ballots[ballotId].maxChoices = _maxChoices;
        emit VoteStarted(ballotId);
    }

    function castVote(uint256 ballotId, uint256[] memory selectedOptions) public {
        require(ballots[ballotId].votingOpen, "Voting is not open");
        require(!ballots[ballotId].hasVoted[msg.sender], "Already voted");
        require(selectedOptions.length <= ballots[ballotId].maxChoices, "Too many choices selected");

        Ballot storage ballot = ballots[ballotId];
        for (uint256 i = 0; i < selectedOptions.length; i++) {
            uint256 option = selectedOptions[i];
            require(isValidOption(option, ballot.options), "Invalid option selected");
            ballot.count.optionCounts[option]++;
        }

        ballots[ballotId].hasVoted[msg.sender] = true;
        emit Voted(msg.sender, ballotId, selectedOptions);
    }

    function tallyVotes(uint256 ballotId) public onlyRole(ADMIN_ROLE) {
        require(ballots[ballotId].votingOpen, "Voting is not open");
        ballots[ballotId].votingOpen = false;

        Ballot storage ballot = ballots[ballotId];
        uint256[] memory counts = new uint256[](ballot.options.length);
        for (uint256 i = 0; i < ballot.options.length; i++) {
            counts[i] = ballot.count.optionCounts[ballot.options[i]];
        }

        emit VoteEnded(ballotId, counts);
    }

    function isValidOption(uint256 option, uint256[] memory options) private pure returns (bool) {
        for (uint256 i = 0; i < options.length; i++) {
            if (options[i] == option) {
                return true;
            }
        }
        return false;
    }
}
