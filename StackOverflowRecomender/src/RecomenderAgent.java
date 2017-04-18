
import jade.core.Agent;
import jade.domain.FIPAAgentManagement.FailureException;
import jade.domain.FIPAAgentManagement.NotUnderstoodException;
import jade.domain.FIPAAgentManagement.RefuseException;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.proto.ContractNetResponder;

public class RecomenderAgent extends Agent {
    public RecomenderAgent() {

    }

    protected void setup() {
        System.out.println("Agent " + this.getLocalName() + " waiting for CFP...");
        MessageTemplate template = MessageTemplate.and(MessageTemplate.MatchProtocol("fipa-contract-net"), MessageTemplate.MatchPerformative(3));
        this.addBehaviour(new ContractNetResponder(this, template) {
            protected ACLMessage handleCfp(ACLMessage cfp) throws NotUnderstoodException, RefuseException {
                System.out.println("Agent " + RecomenderAgent.this.getLocalName() + ": CFP received from " + cfp.getSender().getName() + ". Action is " + cfp.getContent());
                int proposal = RecomenderAgent.this.evaluateAction();
                if(proposal > 2) {
                    System.out.println("Agent " + RecomenderAgent.this.getLocalName() + ": Proposing " + proposal);
                    ACLMessage propose = cfp.createReply();
                    propose.setPerformative(11);
                    propose.setContent(String.valueOf(proposal));
                    return propose;
                } else {
                    System.out.println("Agent " + RecomenderAgent.this.getLocalName() + ": Refuse");
                    throw new RefuseException("evaluation-failed");
                }
            }

            protected ACLMessage handleAcceptProposal(ACLMessage cfp, ACLMessage propose, ACLMessage accept) throws FailureException {
                System.out.println("Agent " + RecomenderAgent.this.getLocalName() + ": Proposal accepted");
                if(RecomenderAgent.this.performAction()) {
                    System.out.println("Agent " + RecomenderAgent.this.getLocalName() + ": Action successfully performed");
                    ACLMessage inform = accept.createReply();
                    inform.setPerformative(7);
                    return inform;
                } else {
                    System.out.println("Agent " + RecomenderAgent.this.getLocalName() + ": Action execution failed");
                    throw new FailureException("unexpected-error");
                }
            }

            protected void handleRejectProposal(ACLMessage cfp, ACLMessage propose, ACLMessage reject) {
                System.out.println("Agent " + RecomenderAgent.this.getLocalName() + ": Proposal rejected");
            }
        });
    }

    private int evaluateAction() {
        return (int)(Math.random() * 10.0D);
    }

    private boolean performAction() {
        return Math.random() > 0.2D;
    }
}
