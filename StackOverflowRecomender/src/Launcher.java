import jade.core.Runtime;
import jade.core.AID;
import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.wrapper.AgentController;
import jade.wrapper.ContainerController;
import jade.wrapper.StaleProxyException;

import java.util.ArrayList;
import java.util.List;

import static java.lang.Thread.sleep;

/**
 * Created by ei08047 on 18/04/2017.
 */
public class Launcher {
    static public List<AID> agentList = new ArrayList<AID>();
    static public AID activeUser ;

    public Launcher(String[] agents){
        System.out.println("args" + agents.length);
        activeUser = new AID(agents[0],true);

        for (int i = 1; i < agents.length; i++) {
            AID a = new AID(agents[i],true);
            agentList.add(a);
        }
    }

    static public void main(String[] args) throws StaleProxyException, InterruptedException {

        Launcher l = new Launcher(args);
        Runtime rt = Runtime.instance();

        Profile p1 = new ProfileImpl();
        //p1.setParameter(...); // optional
        ContainerController mainContainer = rt.createMainContainer(p1);

        Profile p2 = new ProfileImpl();
        //p2.setParameter(...); // optional
        ContainerController container = rt.createAgentContainer(p2);


        Object[] agentRecArgs = new Object[1];
        Object[] agentActArgs = new Object[4];
        agentActArgs[0] = activeUser.getName();
        for (int i = 0; i < agentList.size(); i++) {
            System.out.println("launching agent " +  agentList.get(i).getName());
            AgentController rec = container.createNewAgent(agentList.get(i).getName() , "RecomenderAgent" , agentRecArgs );
            agentActArgs[i+1]=agentList.get(i).getName();
            rec.start();
        }

        sleep(200);


        AgentController ac1 = mainContainer.createNewAgent("active1",  "ActiveUserAgent" ,agentActArgs );
        ac1.start();


    }


}
