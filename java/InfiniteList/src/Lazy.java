import java.util.Optional;
import java.util.function.Function;
import java.util.function.Supplier;
import java.util.function.Predicate;

class Lazy<T> {
    private final Supplier<? extends T> supplier;
    private Optional<Optional<T>> cache;

    private Lazy(Supplier<? extends T> supplier) {
        this.supplier = supplier;
        this.cache = Optional.<Optional<T>>empty();
    }

    private Lazy(T t) {
        this.supplier = (() -> t);
        this.cache = Optional.<Optional<T>>of(Optional.<T>ofNullable(t));
    }

    static <T> Lazy<T> of(Supplier<? extends T> supplier) {
        return new Lazy<T>(supplier);
    }

    static <T> Lazy<T> ofNullable(T t) {
        // this.cache = Optional.<Optional<T>>of(Optional.<T>ofNullable​(this.supplier.get()));
        return new Lazy<T>(t);
    }

    Optional<T> get() {
        Optional<T> v = this.cache.orElse(Optional.<T>ofNullable(this.supplier.get()));
        this.cache = Optional.<Optional<T>>of(v);
        return v;
    }

    <R> Lazy<R> map(Function<? super T, ? extends R> mapper) {
        return Lazy.<R>of(() -> this.get().map(mapper).orElse(null));
    }

    Lazy<T> filter(Predicate<? super T> predicate) {
        return Lazy.<T>of(() -> Lazy.this.get().filter(predicate).orElse(null));
    }

    @Override
    public String toString() {
        String item = this.cache.map(x -> x.map(y -> y.toString()).orElse("null")).orElse("?");
        return String.format("Lazy[%s]", item);
    }
}