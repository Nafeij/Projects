import java.util.function.*;

interface InfiniteList<T> {

    static <T> InfiniteList<T> generate(Supplier<? extends T> s) {
        return InfiniteListImpl.generate(s);
    }

    static <T> InfiniteList<T> iterate(T seed, UnaryOperator<T> next) {
        return InfiniteListImpl.iterate(seed, next); 
    }

    <R> InfiniteList<R> map(Function<? super T, ? extends R> mapper);
    InfiniteList<T> filter(Predicate<? super T> predicate);
    void forEach(Consumer<? super T> action);
    Object[] toArray();
    InfiniteList<T> limit(long n);
    long count();
    <U> U reduce (U identity, BiFunction<U, ? super T, U> accumulator);
    InfiniteList<T> takeWhile(Predicate<? super T> predicate);
    InfiniteList<T> peek();

    boolean isEmpty();
}
