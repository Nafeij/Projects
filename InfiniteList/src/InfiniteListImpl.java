import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;
import java.util.function.UnaryOperator;
import java.util.function.Consumer;
import java.util.function.BiFunction;
import java.util.stream.IntStream;
import java.util.ArrayList;

public class InfiniteListImpl<T> implements InfiniteList<T> {
    private final Lazy<T> head;
    private final Supplier<InfiniteList<T>> tail;

    private InfiniteListImpl(Lazy<T> head, Supplier<InfiniteList<T>> tail) {
        this.head = head;
        this.tail = tail;
    }

    static <T> InfiniteList<T> generate(Supplier<? extends T> s) {
        return new InfiniteListImpl<T>(Lazy.<T>of(s),
                () -> InfiniteList.<T>generate(s));
    }

    static <T> InfiniteList<T> iterate(T seed, UnaryOperator<T> next) {
        return new InfiniteListImpl<T>(
                Lazy.<T>ofNullable(seed),
                () -> InfiniteList.<T>iterate(next.apply(seed), next)
        );
    }

    public <R> InfiniteList<R> map(Function<? super T, ? extends R> mapper) {
        return new InfiniteListImpl<R>(
                this.head.map(mapper),
                () -> this.tail.get().map(mapper)
        );
    }

    public InfiniteList<T> filter(Predicate<? super T> predicate) {
        return new InfiniteListImpl<T>(
                this.head.filter(predicate),
                () -> this.tail.get().filter(predicate)
        );
    }

    public void forEach(Consumer<? super T> action) {
        this.head.get().ifPresent(action);
        this.tail.get().forEach(action);
    }

    public Object[] toArray() {
        return this.reduce( new ArrayList<>(),
                (array, element) -> {array.add(element); return array;})
                .toArray();
    }

    public InfiniteList<T> limit(long n) {
        if (n > 0) {
            return new InfiniteListImpl<T>(this.head,
                    () -> {
                        long m = n - this.head.get().map(x -> 1).orElse(0);
                        return m < 1 ? new EmptyList<>() : this.tail.get().limit(m);
                    });
        } else {
            return new EmptyList<T>();
        }
    }

    public long count() {
        return (this.head.get().map(x -> 1).orElse(0)) + this.tail.get().count();
    }

    public <U> U reduce(U identity, BiFunction<U, ? super T, U> accumulator) {
        U result = this.head.map(x -> accumulator.apply(identity, x)).get().orElse(identity);
        return this.tail.get().reduce(result, accumulator);
    }


    /*public InfiniteList<T> takeWhile(Predicate<? super T> predicate) {
        Lazy<T> head2 = this.head.filter(predicate);
        return new InfiniteListImpl<>(head2, () -> {
            Supplier<InfiniteList<T>> tail = () -> this.tail.get().takeWhile(predicate);
            Supplier<InfiniteList<T>> empty = () -> new EmptyList<T>();
            return this.head.get().map(x -> head2.map(y -> tail).get().orElse(empty)).orElse(tail).get();
        });
    }*/

    public InfiniteList<T> takeWhile(Predicate<? super T> predicate) {
        Lazy<T> newHead = this.head.filter(predicate);
        return new InfiniteListImpl<>(newHead, () ->
                newHead.get().map(x -> this.tail.get().takeWhile(predicate)).orElse(new EmptyList<T>()));
    }

    public InfiniteList<T> peek() {
        this.head.get()
                .map(Object::toString)
                .ifPresent(System.out::println);
        return this.tail.get();
    }

    public boolean isEmpty() {
        return false;
    }
}