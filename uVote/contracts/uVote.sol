// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract uVote {

    struct Vote {
        mapping(uint256 => uint256) optionCounts; // Counts votes for each option
    }

    struct Ballot {
        mapping(address => bool) hasVoted; // Tracks if an address has voted
        Vote count; // Vote counts for this ballot
        bool votingOpen; // Indicates if the voting is open
        uint256[] options; // Array of option IDs
        uint256 maxChoices; // Maximum number of choices allowed per vote
        address initiator; // Address of the ballot initiator
    }

    mapping(uint256 => Ballot) private ballots;
    uint256 public nextBallotId;

    event VoteStarted(uint256 ballotId);
    event Voted(address indexed voter, uint256 ballotId, uint256[] selectedOptions);
    event VoteEnded(uint256 ballotId, uint256[] optionCounts);
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

    function startVote(uint256[] memory _options, uint256 _maxChoices) public {
        uint256 ballotId = nextBallotId++;
        ballots[ballotId].votingOpen = true;
        ballots[ballotId].options = _options;
        ballots[ballotId].maxChoices = _maxChoices;
        ballots[ballotId].initiator = msg.sender; // Store the address of the ballot initiator
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

    function tallyVotes(uint256 ballotId) public {
        require(ballots[ballotId].votingOpen, "Voting is not open");
        require(msg.sender == ballots[ballotId].initiator, "Only the ballot initiator can tally votes"); // Check if the sender is the ballot initiator
        ballots[ballotId].votingOpen = false;

        Ballot storage ballot = ballots[ballotId];
        uint256[] memory counts = new uint256[](ballot.options.length);
        for (uint256 i = 0; i < ballot.options.length; i++) {
            counts[i] = ballot.count.optionCounts[ballot.options[i]];
        }

        emit VoteEnded(ballotId, counts);
    }

    function getBallotInitiator(uint256 ballotId) public view returns (address) {
        require(ballotId < nextBallotId, "Ballot ID does not exist");
        return ballots[ballotId].initiator;
    }

    function isValidOption(uint256 option, uint256[] memory options) private pure returns (bool) {
        for (uint256 i = 0; i < options.length; i++) {
            if (options[i] == option) {
                return true;
            }
        }
        return false;
    }

    function getOpenBallotIds() public view returns (uint256[] memory) {
        uint256 openBallotCount = 0;

        // First, count how many ballots are open
        for (uint256 i = 0; i < nextBallotId; i++) {
            if (ballots[i].votingOpen) {
                openBallotCount++;
            }
        }

        // Now, collect the IDs of the open ballots
        uint256[] memory openBallots = new uint256[](openBallotCount);
        uint256 currentIndex = 0;
        for (uint256 i = 0; i < nextBallotId; i++) {
            if (ballots[i].votingOpen) {
                openBallots[currentIndex] = i;
                currentIndex++;
            }
        }

        return openBallots;
    }

    function getBallotResults(uint256 ballotId) 
        public 
        view 
        returns (bool votingIsOpen, uint256[] memory options, uint256[] memory counts) 
    {
        require(ballotId < nextBallotId, "Ballot ID does not exist");
        Ballot storage ballot = ballots[ballotId];

        votingIsOpen = ballot.votingOpen;
        options = ballot.options;
        counts = new uint256[](options.length);

        for (uint256 i = 0; i < options.length; i++) {
            counts[i] = ballot.count.optionCounts[options[i]];
        }
        return (votingIsOpen, options, counts);
    }
}
