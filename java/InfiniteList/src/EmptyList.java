import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;
import java.util.function.UnaryOperator;
import java.util.function.Consumer;
import java.util.function.BiFunction;

public class EmptyList<T> implements InfiniteList<T>{

    public <R> InfiniteList<R> map(Function<? super T, ? extends R> mapper) {
        return new EmptyList<R>();
    }

    public InfiniteList<T> filter(Predicate<? super T> predicate) {
        return this;
    }

    public void forEach(Consumer<? super T> action) {}

    public Object[] toArray() {
        return new Object[0];
    }

    public InfiniteList<T> limit(long n) {
        return this;
    }

    public long count() {
        return 0;
    }

    public <U> U reduce(U identity, BiFunction<U, ? super T, U> accumulator) {
        return identity;
    }

    public InfiniteList<T> takeWhile(Predicate<? super T> predicate) {
        return this;
    }

    public InfiniteList<T> peek() {
        return this;
    }

    public boolean isEmpty() {
        return true;
    }
}