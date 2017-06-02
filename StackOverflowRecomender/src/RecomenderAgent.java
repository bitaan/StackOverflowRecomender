
import jade.core.Agent;
import jade.domain.FIPAAgentManagement.FailureException;
import jade.domain.FIPAAgentManagement.NotUnderstoodException;
import jade.domain.FIPAAgentManagement.RefuseException;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.proto.ContractNetResponder;

import java.io.*;
import java.net.Socket;
import java.util.ArrayList;

public class RecomenderAgent extends Agent {
    public RecomenderAgent() {

    }

    protected void setup() {
        System.out.println("Agent " + this.getLocalName() + " waiting for CFP...");
        MessageTemplate template = MessageTemplate.and(MessageTemplate.MatchProtocol("fipa-contract-net"), MessageTemplate.MatchPerformative(3));

        this.addBehaviour(new ContractNetResponder(this, template) {
            protected ACLMessage handleCfp(ACLMessage cfp) throws NotUnderstoodException, RefuseException {
                System.out.println("Agent " + RecomenderAgent.this.getLocalName() + ": CFP received from " + cfp.getSender().getName() + ". Action is " + cfp.getContent());

                String content = cfp.getContent();
                String[] split = content.split(" ");
                int id=  Integer.parseInt( split[0]);
                int setSize = Integer.parseInt( split[1]);
                //send
                String hostName = "localhost";
                int portNumber = 8888;
                Socket socket = null;
                PrintWriter out = null;
                try {
                    socket = new Socket(hostName, portNumber);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                    out = new PrintWriter(socket.getOutputStream(), true);
                } catch (IOException e) {
                    e.printStackTrace();
                }

                String s = ""+ id + " " + setSize;
                out.print(s);
                out.flush();
                //receive
                InputStream istream = null;
                try {
                    istream = socket.getInputStream();
                } catch (IOException e) {
                    e.printStackTrace();
                }

                BufferedReader receiveRead = new BufferedReader(new InputStreamReader(istream));
                String receiveMessage;

                String response="";
                try {
                    for (int i = 0; i < 10; i++) {
                        receiveMessage = receiveRead.readLine();
                        response += receiveMessage + '\n';
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }

                System.out.println("//////////////////////end///////////////////////////////////////");

                int proposal = RecomenderAgent.this.evaluateAction();
                if(proposal > 2) {
                    System.out.println("Agent " + RecomenderAgent.this.getLocalName() + ": Proposing " + proposal);
                    ACLMessage propose = cfp.createReply();
                    propose.setPerformative(11);
                    propose.setContent(response);
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


    //TODO: replace this function by something that uses user similarity to this Recomender agent that acts as a cluster representative
    private int evaluateAction() {
        return 3;
        //(int)(Math.random() * 10.0D);
    }


    // check if there are recomendation items
    private boolean performAction() {
        return true;
        //Math.random() > 0.2D;
    }
}
