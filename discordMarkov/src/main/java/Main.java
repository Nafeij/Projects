import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.entities.TextChannel;
import net.dv8tion.jda.api.exceptions.InsufficientPermissionException;
import org.apache.commons.text.StringEscapeUtils;

import javax.annotation.RegEx;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Objects;


public class Main {

    private static final String FILENAME = "msgs.txt";

    public static void main(String[] args) {
        JDA api;
        try {
            api = JDABuilder.createDefault("<SECRET TOKEN>").build();
            System.out.println(api.awaitReady().getGuilds().size());
            List<TextChannel> textChannels = api.getTextChannels();
            System.out.println(textChannels.size());
            //System.out.println(api.getTextChannelById(952807349796610080L).getHistoryFromBeginning(1).complete().getRetrievedHistory().get(0).getContentRaw());

            Iterator<String> mIterator = api.awaitReady().getTextChannels().stream()
                    .flatMap(x -> messageGetter(x, 500).stream().map(Message::getContentStripped).filter(s -> !(s.isEmpty() || s.matches("\\s+"))))
                    .iterator();

            Files.write(Paths.get(FILENAME), (Iterable<String>) () -> mIterator);

            //mIterator.forEachRemaining(i -> {if (i.equals("")) System.out.println("Null");});

            // System.out.println(api.getTextChannelById(945216662691520535L).getHistoryFromBeginning(1).complete().getRetrievedHistory().get(0).getContentRaw());
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private static List<Message> messageGetter(TextChannel channel, int limit) {
        List<Message> sum_messages = new ArrayList<>(), messages = new ArrayList<>();
        long last_id = -1L;
        int fetchLimit = 100;

        while (true) {
            try {
                if (last_id == -1L) {
                    messages = channel.getHistoryFromBeginning(fetchLimit).complete()
                            .getRetrievedHistory();
                } else {
                    messages = channel.getHistoryBefore(last_id, fetchLimit).complete()
                            .getRetrievedHistory();
                }
            } catch (InsufficientPermissionException e){
                System.out.println(channel.getName());
                break;
            }
            sum_messages.addAll(messages);
            if (messages.size() < fetchLimit || sum_messages.size() >= limit) break;
            last_id = messages.get(messages.size() - 1).getIdLong();
        }

        return sum_messages;
    }
}
